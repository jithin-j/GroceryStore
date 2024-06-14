## Grocery Store V2

### Overview

This document outlines the design of a grocery store application. The application aims to provide users with a convenient platform for browsing and purchasing groceries. It comprises several key components:

* User Management: Handles user registration, authentication, and authorization.
* Product Catalog: Manages product information, including sections, names, prices, and quantities.
* Shopping Cart: Allows users to add, remove, and manage items before checkout.
* Order Processing: Processes user orders and manages inventory updates.
* Administration: Provides functionalities for managing sections, products, user requests, and reports.

### Models

The system utilizes several models to represent data entities:

* **User** (id, username, password, role, status, last_activity)
* **Section** (id, name)
* **Product** (id, section_id, name, unit_type, rate_per_unit, quantity_available)
* **SectionRequest** (id, request_type, section_id, section_name, status)
* **Order** (id, user_id, items, timestamp)
* **OrderItem** (id, order_id, product_id, product_name, quantity, price)

### System Design

* **Frontend:** Vue.js (Handles user interface and interaction)
* **Backend:** Flask (Provides application logic and API endpoints)
* **Database:** SQLite (Stores application data - lightweight and for development)
* **Caching:** Redis (Improves performance by caching frequently accessed data)
* **Background Jobs:**
    * Redis (Stores tasks for asynchronous processing)
    * Celery (Manages worker processes to execute background tasks, e.g., order processing)

### User Management

* Users have roles: "admin," "store manager," "user."
* Status can be "approved" or "pending."
* Last activity is tracked for user engagement analysis.

### Product and Section Management

* Products are categorized into sections.
* Detailed attributes are defined for sections and products.

### Section Request Management

* Users can request creation or modification of sections.
* Requests track request type, section details, and status.

### Order Management

* Orders capture user purchases with a unique identifier and timestamp.
* Orders consist of multiple order items, linking products and quantities.
