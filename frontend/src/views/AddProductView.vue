<template>
    <div class="add-product-container">
        <h2>Add Product to Section</h2>
        <form @submit.prevent="addProduct" class="add-product-form">
            <div class="form-group">
                <label for="productName">Product Name:</label>
                <input type="text" id="productName" v-model="productName" required>
            </div>
            <div class="form-group">
                <label for="unitType">Unit Type:</label>
                <select id="unitType" v-model="unitType">
                    <option value="Rs/Kg">Rs/Kg</option>
                    <option value="Rs/Litre">Rs/Litre</option>
                    <option value="Rs/Dozen">Rs/Dozen</option>
                    <option value="Rs/Gram">Rs/Gram</option>
                </select>
            </div>
            <div class="form-group">
                <label for="ratePerUnit">Rate per Unit:</label>
                <input type="number" id="ratePerUnit" v-model="ratePerUnit" required>
            </div>
            <div class="form-group">
                <label for="quantityAvailable">Quantity Available:</label>
                <input type="number" id="quantityAvailable" v-model="quantityAvailable" required>
            </div>
            <div class="form-group">
                <label for="sectionId">Section:</label>
                <select id="sectionId" v-model="sectionId">
                    <option v-for="section in sections" :key="section.id" :value="section.id">
                        {{ section.name }}
                    </option>
                </select>
            </div>
            <div class="form-group">
                <button type="submit">Add Product</button>
            </div>
        </form>
    </div>
</template>

<style scoped>
.add-product-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 5px;
}

.add-product-form {
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
    background-color: #2ecc71;
    color: white;
    padding: 10px;
    border: none;
    border-radius: 3px;
    cursor: pointer;
}

button:hover {
    background-color: #27ae60;
}
</style>

<script>
import axios from "axios";

export default {
    data() {
        return {
            productName: "",
            unitType: "",
            ratePerUnit: 0,
            quantityAvailable: 0,
            sectionId: null, // Initialize sectionId with null
            sections: [], // Store the list of sections
        };
    },
    created() {
        // Fetch the list of sections
        axios.get("/api/sections", {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            },
        }).then((response) => {
            this.sections = response.data;
        }).catch((error) => {
            console.error("Failed to fetch sections:", error);
        });
    },
    methods: {
        addProduct() {
            // Get the JWT token from local storage
            const jwtToken = localStorage.getItem("access_token");

            // Set the authorization header with the JWT token
            const config = {
                headers: {
                    Authorization: `Bearer ${jwtToken}`,
                },
            };

            // Create the payload
            const data = {
                name: this.productName,
                unit_type: this.unitType,
                rate_per_unit: this.ratePerUnit,
                quantity_available: this.quantityAvailable,
                section_id: this.sectionId, // Use the selected section ID
            };

            // Make the POST request with the token and data
            axios
                .post(`/api/sections/${this.sectionId}/add-product`, data, config)
                .then((response) => {
                    // Product added successfully, you can handle the response here
                    console.log("Product added:", response.data);
                    // Optionally, you can navigate to another page after adding the product
                    this.$router.push(`/manager/dashboard`);
                })
                .catch((error) => {
                    console.error("Failed to add product:", error);
                });
        },
    },
};
</script>
