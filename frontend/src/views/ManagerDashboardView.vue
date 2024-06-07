<template>
    <div class="sections-products-container">
        <button @click="logout" class="logout-button">Logout</button>
        <h2>Sections and Products</h2>
        <div v-for="section in sections" :key="section.id" class="section-container">
            <h3>{{ section.name }}</h3>
            <RouterLink :to="{ name: 'edit-section-request', params: { sectionId: section.id } }" class="edit-section-link">
                Edit or Delete Section
            </RouterLink>
            <ul class="product-list">
                <li v-for="product in section.products" :key="product.id" class="product-item">
                    {{ product.name }} - {{ product.unit_type }} - Rate: {{ product.rate_per_unit }} - Quantity: {{
                        product.quantity_available }}
                    <button @click="editProduct(product.id)" class="action-button">Edit</button>
                    <button @click="deleteProduct(product.id)" class="action-button">Delete</button>
                </li>
            </ul>
        </div>
        <RouterLink to="/product/add" class="add-product-link">Add a new product</RouterLink>
        <br/>
        <RouterLink to="/request/section" class="request-section-link">Request for a new section</RouterLink>
        <br/>
        <button @click="exportCSV" class="export-csv-button">Export CSV</button>

        <!-- Link to download the CSV once it's ready -->
        <a v-if="csvReady" :href="csvDownloadLink" download="product_export.csv" class="download-csv-link">
          Download CSV
        </a>
    </div>
</template>

<script>
import axios from "axios";
import { RouterLink } from "vue-router";

export default {
    data() {
        return {
            sections: [],
            csvReady: false,
            csvDownloadLink: '',
        };
    },
    mounted() {
        this.fetchSections();
    },
    methods: {
        fetchSections() {
            axios.get("/api/sections", {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('access_token')}`
                }
            }).then((response) => {
                this.sections = response.data;
            });
        },
        async exportCSV() {
            try {
                // Make a request to the backend to trigger CSV export
                const response = await axios.post('/export-csv', {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('access_token')}`
                    }
                });

                // Display a success message or handle as needed
                console.log(response.data.message);

                // Set a flag indicating that the CSV is ready for download
                this.csvReady = true;

                // Provide the download link
                this.csvDownloadLink = 'http://127.0.0.1:5000/download-csv';
            } catch (error) {
                // Handle errors
                console.error('Error exporting CSV:', error.message);
            }
        },
        deleteProduct(productId) {
            if (confirm("Are you sure you want to delete this product?")) {
                axios.delete(`/api/products/${productId}`, {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('access_token')}`
                    }
                }).then(() => {
                    // Product deleted successfully, refresh the sections
                    this.fetchSections();
                }).catch((error) => {
                    console.error("Failed to delete product:", error);
                });
            }
        },
        editProduct(productId){
            this.$router.push(`/edit/${productId}`);
        },
        logout() {
            // Remove the access token from local storage
            localStorage.removeItem('access_token');

            // Redirect to the login page or any other desired page after logout
            this.$router.push('/manager/login');
        },
    },
    components: { RouterLink }
};
</script>

<style scoped>
.sections-products-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 5px;
}

.logout-button {
    background-color: #e74c3c;
    color: white;
    padding: 10px;
    border: none;
    border-radius: 3px;
    cursor: pointer;
    margin-bottom: 20px;
}

.logout-button:hover {
    background-color: #c0392b;
}

.section-container {
    margin-top: 20px;
}

.edit-section-link,
.add-product-link,
.request-section-link,
.export-csv-button,
.action-button {
    background-color: #3498db;
    color: white;
    padding: 10px;
    border: none;
    border-radius: 3px;
    cursor: pointer;
    margin-right: 10px;
    text-decoration: none;
    display: inline-block;
    margin: 2px;
}

.edit-section-link:hover,
.add-product-link:hover,
.request-section-link:hover,
.export-csv-button:hover,
.action-button:hover {
    background-color: #2980b9;
}

.product-list {
    list-style: none;
    padding: 0;
}

.product-item {
    margin-bottom: 10px;
    padding-bottom: 5px;
    border-bottom: 1px solid #ddd;
}

.download-csv-link {
    display: block;
    margin-top: 10px;
    text-decoration: none;
    color: #2ecc71;
}</style>