<template>
    <div class="edit-product-container">
        <h2>Edit Product</h2>
        <form @submit.prevent="updateProduct" class="edit-product-form">
            <div class="form-group">
                <label for="name">Product Name:</label>
                <input type="text" id="name" v-model="product.name" required>
            </div>
            <div class="form-group">
                <label for="unitType">Unit Type:</label>
                <select id="unitType" v-model="product.unit_type" required>
                    <option value="Rs/Kg">Rs/Kg</option>
                    <option value="Rs/Litre">Rs/Litre</option>
                    <option value="Rs/Dozen">Rs/Dozen</option>
                    <option value="Rs/Gram">Rs/Gram</option>
                </select>
            </div>
            <div class="form-group">
                <label for="ratePerUnit">Rate per Unit:</label>
                <input type="number" id="ratePerUnit" v-model="product.rate_per_unit" required>
            </div>
            <div class="form-group">
                <label for="quantityAvailable">Quantity Available:</label>
                <input type="number" id="quantityAvailable" v-model="product.quantity_available" required>
            </div>
            <div class="form-group">
                <button type="submit">Update Product</button>
            </div>
        </form>
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </div>
</template>

<style scoped>
.edit-product-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 5px;
}

.edit-product-form {
    display: grid;
    grid-gap: 15px;
}

.form-group {
    margin-bottom: 15px;
}

label {
    display: block;
    margin-bottom: 5px;
}

input,
select {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
}

button {
    background-color: #3498db;
    color: white;
    padding: 10px;
    border: none;
    border-radius: 3px;
    cursor: pointer;
}

button:hover {
    background-color: #2980b9;
}

.error-message {
    color: #e74c3c;
    margin-top: 10px;
}
</style>

<script>
import axios from "axios";
export default {
    data() {
        return {
            product: {
                name: '',
                unit_type: 'Rs/Kg',
                rate_per_unit: 0,
                quantity_available: 0
            },
            errorMessage: ''
        };
    },
    created() {
        // Fetch the product details from the API and populate the product object
        // You can use the route parameter (productId) to make an API request to get the current product data.
        const productId = this.$route.params.productId; // Assuming you have a route parameter named 'productId'

        axios
            .get(`/api/products/${productId}`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('access_token')}`
                }
            })
            .then((response) => {
                this.product = response.data; // Assuming the API returns product details
            })
            .catch((error) => {
                console.error("Failed to fetch product details:", error);
            });
    },
    methods: {
        updateProduct() {
            // Send a PUT request to update the product details
            // Include the product object in the request data
            // Handle success and error responses as needed
            const productId = this.$route.params.productId; // Assuming you have a route parameter named 'productId'

            axios
                .put(`/api/products/${productId}`, this.product, {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('access_token')}`
                    }
                })
                .then((response) => {
                    if (response.status === 200) {
                        // Handle the success case, e.g., show a success message or redirect to another page
                        this.$router.push('/manager/dashboard'); // Redirect to the products page
                    }
                })
                .catch((error) => {
                    // Handle the error case, e.g., show an error message
                    console.log(error);
                    this.errorMessage = 'Failed to update product. Please try again.';
                });
        }
    }
};
</script>
