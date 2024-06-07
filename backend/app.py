from flask import Flask, jsonify, request, abort, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    create_access_token,
    JWTManager,
    get_jwt_identity,
    jwt_required,
    verify_jwt_in_request,
)
from functools import wraps
import os
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
from celery import Celery
import csv
from redis import Redis
import json


current_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SECRET_KEY"] = "my-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    current_dir, "database.db"
)
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/0"
app.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/0"
db = SQLAlchemy(app)
CORS(app, origins="*")
jwt = JWTManager(app)
scheduler = BackgroundScheduler()
redis_client = Redis.from_url("redis://localhost:6379/0")

# logging.basicConfig()
# logging.getLogger("apscheduler").setLevel(logging.DEBUG)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(20), default="user")  # Default role is 'user'
    status = db.Column(
        db.String(20), default="approved"
    )  # Default status is 'approved'
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)

    def update_last_activity(self):
        self.last_activity = datetime.utcnow()


class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey("section.id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    unit_type = db.Column(db.String(50), nullable=False)
    rate_per_unit = db.Column(db.Float, nullable=False)
    quantity_available = db.Column(db.Integer, nullable=False)


class SectionRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_type = db.Column(db.String(20), nullable=False)
    section_id = db.Column(
        db.Integer, db.ForeignKey("section.id")
    )  # Foreign key to Section
    section = db.relationship(
        "Section", backref="section_requests"
    )  # Relationship to Section
    section_name = db.Column(db.String(100))
    status = db.Column(db.String(20), default="pending")

    def __init__(self, request_type, section_id=None, section_name=None):
        self.request_type = request_type
        self.section_id = section_id
        self.section_name = section_name

    def to_dict(self):
        return {
            "id": self.id,
            "request_type": self.request_type,
            "section_id": self.section_id,
            "section_name": self.section_name,
            "status": self.status,
        }


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    items = db.relationship("OrderItem")
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    product_name = db.Column(db.String(255), db.ForeignKey("product.name"))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)


celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)


def fetch_user_role(user_identity):
    user = User.query.filter_by(username=user_identity).first()
    if user:
        return user.role
    return None


# def role_required(role):
#   def decorator(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#       verify_jwt_in_request()
#       user_identity = get_jwt_identity()
#       user_role = fetch_user_role(user_identity)
#       if user_role is None or user_role != role:
#             return abort(403, description='Unauthorized')
#       return f(*args, **kwargs)
#     return decorated
#   return decorator


def role_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            verify_jwt_in_request()
            user_identity = get_jwt_identity()
            user_role = fetch_user_role(user_identity)
            if user_role is None or user_role not in roles:
                return abort(403, description="Unauthorized")
            return f(*args, **kwargs)

        return decorated

    return decorator


def safe_str_cmp(a, b):
    try:
        return a.__eq__(b)
    except AttributeError:
        return False


@app.route("/signup/user", methods=["POST"])
def signup_user():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        return jsonify({"message": "Invalid data"}), 400

    user = User(username=username, password=password, role="user", status="approved")
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User account created"}), 201


@app.route("/signup/manager", methods=["POST"])
def signup_manager():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        return jsonify({"message": "Invalid data"}), 400

    user = User(
        username=username, password=password, role="store manager", status="pending"
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Manager account creation pending admin approval"})


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(username=username).first()

    if not user or not safe_str_cmp(user.password, password) or user.role != "user":
        return jsonify({"message": "Invalid credentials"}), 401

    if user.status == "pending":
        return jsonify({"message": "Account pending admin approval"}), 401
    user.update_last_activity()
    db.session.commit()
    access_token = create_access_token(
        identity=username, additional_claims={"role": user.role}
    )
    return jsonify(access_token=access_token), 200


@app.route("/manager/login", methods=["POST"])
def manager_login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(username=username).first()

    if (
        not user
        or not safe_str_cmp(user.password, password)
        or user.role != "store manager"
    ):
        return jsonify({"message": "Invalid credentials"}), 401

    if user.status == "pending":
        return jsonify({"message": "Account pending admin approval"}), 401

    user.update_last_activity()
    db.session.commit()
    access_token = create_access_token(
        identity=username, additional_claims={"role": user.role}
    )
    return jsonify(access_token=access_token), 200


@app.route("/admin/login", methods=["POST"])
def admin_login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(username=username).first()

    if not user or not safe_str_cmp(user.password, password) or user.role != "admin":
        return jsonify({"message": "Invalid credentials"}), 401

    user.update_last_activity()
    db.session.commit()
    access_token = create_access_token(
        identity=username, additional_claims={"role": user.role}
    )
    return jsonify(access_token=access_token), 200


@app.route("/api/manager-accounts/pending", methods=["GET"])
@role_required(["admin"])
def get_pending_manager_accounts():
    # Query the database for manager accounts with status 'pending'
    pending_manager_accounts = User.query.filter_by(
        role="store manager", status="pending"
    ).all()

    # Convert the accounts to a list of dictionaries
    manager_account_list = [
        {"id": account.id, "username": account.username, "status": account.status}
        for account in pending_manager_accounts
    ]

    return jsonify(manager_account_list), 200


@app.route("/admin/approve_manager/<int:user_id>/approve", methods=["POST"])
@role_required(["admin"])
def approve_manager(user_id):
    user = User.query.get(user_id)
    if user:
        user.status = "approved"
        db.session.commit()
        return jsonify({"message": "Manager account approved"})
    return jsonify({"message": "User not found"}), 404


@app.route("/admin/approve_manager/<int:user_id>/reject", methods=["POST"])
@role_required(["admin"])
def reject_manager(user_id):
    user = User.query.get(user_id)
    if user:
        user.status = "rejected"
        db.session.commit()
        return jsonify({"message": "Manager account rejected"})
    return jsonify({"message": "User not found"}), 404


@app.route("/manager")
@role_required(["store manager"])
def manager():
    return jsonify({"message": "Hello from the manager page"})


@app.route("/api/sections/add", methods=["POST"])
@role_required(["admin"])
def add_section():
    name = request.json.get("name", None)
    if not name:
        return jsonify({"message": "Invalid data"}), 400

    section = Section(name=name)
    db.session.add(section)
    db.session.commit()

    return jsonify({"message": "Section added"}), 201


@app.route("/api/sections", methods=["GET"])
@role_required(["admin", "store manager", "user"])
def get_sections_with_products():
    # Check if the data is already cached
    cache_key = "sections_with_products"
    cached_data = redis_client.get(cache_key)

    if cached_data:
        # If cached data exists, use it directly
        sections_with_products = json.loads(cached_data)
    else:
        # If no cached data, fetch from the database
        sections = db.session.query(Section).all()

        sections_with_products = []

        for section in sections:
            products = db.session.query(Product).filter_by(section_id=section.id).all()

            products_data = [
                {
                    "id": product.id,
                    "name": product.name,
                    "unit_type": product.unit_type,
                    "rate_per_unit": product.rate_per_unit,
                    "quantity_available": product.quantity_available,
                    "section_id": section.id,
                }
                for product in products
            ]

            section_data = {
                "id": section.id,
                "name": section.name,
                "products": products_data,
            }

            sections_with_products.append(section_data)

        # Cache the fetched data for future use
        redis_client.setex(cache_key, 10, json.dumps(sections_with_products))

    return jsonify(sections_with_products)


# Without Caching
# def get_sections_with_products():
#     sections = db.session.query(Section).all()

#     sections_with_products = []

#     for section in sections:
#         products = db.session.query(Product).filter_by(section_id=section.id).all()

#         products_data = [
#             {
#                 "id": product.id,
#                 "name": product.name,
#                 "unit_type": product.unit_type,
#                 "rate_per_unit": product.rate_per_unit,
#                 "quantity_available": product.quantity_available,
#                 "section_id": section.id,
#             }
#             for product in products
#         ]

#         section_data = {
#             "id": section.id,
#             "name": section.name,
#             "products": products_data,
#         }

#         sections_with_products.append(section_data)

#     return jsonify(sections_with_products)


@app.route("/api/sections/<string:section_id>", methods=["GET", "PUT", "DELETE"])
@role_required(["admin"])
def section_by_id(section_id):
    section = Section.query.get(section_id)
    if section is None:
        return jsonify({"message": "Section not found"}), 404

    if request.method == "GET":
        # GET method: Retrieve section details
        section_data = {
            "id": section.id,
            "name": section.name,
            # Add other fields as needed
        }
        return jsonify(section_data)

    elif request.method == "PUT":
        # PUT method: Edit section details
        data = request.get_json()
        section.name = data.get("name", section.name)
        # Update other fields as needed

        db.session.commit()
        return jsonify({"message": "Section updated successfully"})

    elif request.method == "DELETE":
        # DELETE method: Delete the section
        db.session.delete(section)
        db.session.commit()
        return jsonify({"message": "Section deleted successfully"})


@app.route("/api/sections/<string:section_id>/add-product", methods=["POST"])
@role_required(["store manager"])
def add_product_to_section(section_id):
    data = request.get_json()

    # Check if the required fields are in the request data
    required_fields = ["name", "unit_type", "rate_per_unit", "quantity_available"]
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"'{field}' is required"}), 400

    # Check if the section with the specified ID exists
    section = Section.query.get(section_id)
    if not section:
        return jsonify({"message": "Section not found"}), 404

    # Create a new product for the section
    new_product = Product(
        name=data["name"],
        unit_type=data["unit_type"],
        rate_per_unit=data["rate_per_unit"],
        quantity_available=data["quantity_available"],
        section_id=data["section_id"],
    )

    db.session.add(new_product)
    db.session.commit()

    return (
        jsonify(
            {"message": "Product added successfully", "product_id": new_product.id}
        ),
        201,
    )


@app.route("/api/products/<string:product_id>", methods=["GET", "PUT", "DELETE"])
@role_required(["store manager"])  # Add any required role decorator
def get_put_or_delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    if request.method == "GET":
        # Handle GET request to retrieve product details
        product_data = {
            "id": product.id,
            "name": product.name,
            "unit_type": product.unit_type,
            "rate_per_unit": product.rate_per_unit,
            "quantity_available": product.quantity_available,
        }
        return jsonify(product_data)

    elif request.method == "PUT":
        # Handle PUT request to update product details
        data = request.get_json()

        # Update the product details with the data from the request
        product.name = data.get("name", product.name)
        product.unit_type = data.get("unit_type", product.unit_type)
        product.rate_per_unit = data.get("rate_per_unit", product.rate_per_unit)
        product.quantity_available = data.get(
            "quantity_available", product.quantity_available
        )

        # Commit the changes to the database
        db.session.commit()

        return jsonify({"message": "Product updated successfully"})

    elif request.method == "DELETE":
        # Handle DELETE request to delete the product
        # Check if the user has permission to delete the product
        # You might need additional authorization logic here

        # Delete the product from the database
        db.session.delete(product)
        db.session.commit()

        return jsonify({"message": "Product deleted successfully"})


@app.route("/api/section-requests", methods=["POST"])
@role_required("store manager")
def submit_section_request():
    data = request.get_json()
    request_type = data.get("request_type")
    section_id = data.get("section_id")
    section_name = data.get("section_name")

    if not request_type:
        return jsonify({"message": "Request type is required"}), 400

    section_request = SectionRequest(
        request_type=request_type, section_id=section_id, section_name=section_name
    )
    db.session.add(section_request)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Section request submitted successfully",
                "request_id": section_request.id,
            }
        ),
        201,
    )


# Admins can retrieve a list of section requests
@app.route("/api/section-requests", methods=["GET"])
@role_required(["admin"])
def get_section_requests():
    section_requests = SectionRequest.query.all()
    section_requests_data = [
        request.to_dict() for request in section_requests if request.status == "pending"
    ]
    return jsonify(section_requests_data)


# Admins can approve a section request
@app.route("/api/section-requests/approve/<int:request_id>", methods=["PUT"])
@role_required(["admin"])
def approve_section_request(request_id):
    section_request = SectionRequest.query.get(request_id)

    if not section_request:
        return jsonify({"message": "Section request not found"}), 404

    if section_request.request_type == "create":
        # Create a new section
        new_section = Section(name=section_request.section_name)
        db.session.add(new_section)

    elif section_request.request_type == "edit":
        section = Section.query.get(section_request.section_id)
        if not section:
            return jsonify({"message": "Section not found"}), 404
        section.name = section_request.section_name

    elif section_request.request_type == "delete":
        section = Section.query.get(section_request.section_id)
        if not section:
            return jsonify({"message": "Section not found"}), 404
        db.session.delete(section)

    section_request.status = "approved"
    db.session.commit()

    return jsonify({"message": "Section request approved successfully"})


# Admins can reject a section request
@app.route("/api/section-requests/reject/<int:request_id>", methods=["PUT"])
@role_required(["admin"])
def reject_section_request(request_id):
    section_request = SectionRequest.query.get(request_id)

    if not section_request:
        return jsonify({"message": "Section request not found"}), 404

    section_request.status = "rejected"
    db.session.commit()

    return jsonify({"message": "Section request rejected successfully"})


@app.route("/buy-items", methods=["POST"])
@role_required(["user"])
def buy_items():
    data = request.get_json()
    user_identity = (
        get_jwt_identity()
    )  # Retrieve the user's identity from the token (username in this case)
    user = User.query.filter_by(username=user_identity).first()
    user_id = user.id
    items = data["items"]

    order = Order(user_id=user_id)
    db.session.add(order)
    user.update_last_activity()
    db.session.commit()

    for item in items:
        product_id = item["product_id"]
        quantity = item["quantity"]
        product_name = item["productName"]
        price = item["price"]

        order_item = OrderItem(
            order_id=order.id,
            product_id=product_id,
            quantity=quantity,
            product_name=product_name,
            price=price,
        )
        db.session.add(order_item)

        product = Product.query.get(product_id)
        product.quantity_available -= quantity
        db.session.commit()

    return "Items bought and database updated!"


@app.route("/api/user/order-history")
@role_required(["user"])
def get_user_order_history():
    user_identity = get_jwt_identity()
    user = User.query.filter_by(username=user_identity).first()
    if not user:
        return jsonify({"message": "User not found"}), 404
    user_id = user.id
    orders = Order.query.filter_by(user_id=user_id).all()

    order_history = []
    for order in orders:
        order_data = {
            "order_id": order.id,
            "timestamp": order.timestamp,
            "items": [
                {
                    "product_name": item.product_name,
                    "quantity": item.quantity,
                    "price": item.price,
                }
                for item in order.items
            ],
        }
        order_history.append(order_data)

    return jsonify(order_history)


# @app.route('/api/sections', methods=['GET'])
# @role_required(['store manager'])
# def get_sections():
#     try:
#         # Query all sections from the database
#         sections = Section.query.all()

#         # Create a list to store the section data
#         sections_data = []

#         # Iterate through sections and create a dictionary for each section
#         for section in sections:
#             section_data = {
#                 'id': section.id,
#                 'name': section.name,
#             }
#             sections_data.append(section_data)

#         # Return the sections as JSON response
#         return jsonify(sections_data)
#     except Exception as e:
#         return jsonify({"message": "Failed to retrieve sections", "error": str(e)}), 500


@app.route("/api/data")
def get_data():
    data = {"message": "Hello from the Flask backend!"}
    return jsonify(data)


def send_email(receiver_email, subject, body):
    sender_email = "grocerystoreiitm2@gmail.com"  # Your Gmail
    password = "yzkh ozgx gzop qsfg"  # Your Gmail password

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()


def send_reminders():
    # Logic to identify inactive users and send reminder emails
    # Fetch inactive users
    # inactive_users = User.query.filter(
    #     User.last_activity < datetime.now() - timedelta(days=1)
    # ).all()

    # for user in inactive_users:
    #     send_email(
    #         user.email,
    #         "Reminder: Visit or Buy!",
    #         "Please visit our website or check out our latest products.",
    #     )
    print("Scheduler started at:", datetime.now())
    send_email(
        "jithinjagadeesh1@gmail.com",
        "Reminder: Visit or Buy!",
        "Please visit our website or check out our latest products.",
    )


def send_email_report(receiver_email, subject, body):
    # Replace with your email configuration
    sender_email = "grocerystoreiitm2@gmail.com"
    sender_password = "yzkh ozgx gzop qsfg"

    # Set up the MIME
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))

    # Connect to the SMTP server
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()

        # Log in with your email and password
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, receiver_email, message.as_string())


def monthly_activity_report():
    # Fetch all users and their orders for the previous month
    today = datetime.now()
    # last_month_start = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
    # last_month_end = last_month_start.replace(
    #     day=1, month=last_month_start.month + 1
    # ) - timedelta(days=1)
    last_month_start = today.replace(day=1)
    last_month_end = today
    print(last_month_start, last_month_end)
    with app.app_context():
        users = User.query.all()

        # Create a report for each user
        for user in users:
            if user.role != "user":
                continue

            orders = (
                Order.query.filter_by(user_id=user.id)
                .filter(
                    Order.timestamp >= last_month_start,
                    Order.timestamp <= last_month_end,
                )
                .all()
            )

            # Calculate the total amount for the user's orders
            total_amount = 0
            order_details = ""

            for order in orders:
                for order_item in order.items:
                    # Calculate the amount for each order item
                    amount = order_item.quantity * order_item.price
                    total_amount += amount

                    # Add details of each order item
                    order_details += f"<li>{order_item.product_name} - Quantity: {order_item.quantity} - Amount: ${amount:.2f}</li>"

            # Generate an HTML report
            html_report = f"""
            <html>
                <head></head>
                <body>
                    <h1>Monthly Activity Report - {user.username}</h1>
                    <p>Total Expenditure: ${total_amount:.2f}</p>
                    <ul>
                        <!-- Add details of each order item -->
                        {order_details}
                    </ul>
                </body>
            </html>
            """

            # Send the report as an email to the user's email address
            send_email_report(
                "jithinjagadeesh1@gmail.com", "Monthly Activity Report", html_report
            )


scheduler.add_job(send_reminders, "cron", hour=18, minute=00)  # 6:00 PM every day
# scheduler.add_job(
#     monthly_activity_report, "cron", day=1, hour=6
# )  # 6:00 AM on 1st day of every month
scheduler.add_job(monthly_activity_report, "cron", hour=19, minute=8)
scheduler.start()


def export_to_csv(products):
    fields = ["Name", "Stock Remaining", "Description", "Price"]
    data = [
        {
            "Name": product.name,
            "Stock Remaining": product.quantity_available,
            "Description": product.unit_type,
            "Price": product.rate_per_unit,
        }
        for product in products
    ]

    with open("product_export.csv", "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)


@celery.task
def export_csv_async():
    with app.app_context():
        products = Product.query.all()
        print("Query finished")
        export_to_csv(products)
        return {"message": "CSV Export Finished"}


@app.route("/export-csv", methods=["POST"])
# @role_required(["store manager"])
def export_csv():
    # Trigger async job to export CSV
    export_csv_async.delay()

    return jsonify({"message": "CSV Export Started"})


@app.route("/download-csv")
def download_csv():
    try:
        # Serve the CSV file for download
        return send_from_directory(".", "product_export.csv", as_attachment=True)
    except Exception as e:
        return jsonify({"message": f"Error downloading CSV: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
