<template>
    <div class="sections-and-products-container">
        <h2>Sections and Products</h2>
        <div v-for="section in sections" :key="section.id" class="section-container">
            <h3>{{ section.name }}</h3>
            <ul class="products-list">
                <li v-for="product in section.products" :key="product.id" class="product-item">
                    {{ product.name }} - {{ product.unit_type }} - Rate: {{ product.rate_per_unit }} - Quantity: {{
                        product.quantity_available }}
                </li>
            </ul>
            <div class="section-buttons">
                <button @click="editSection(section.id)" class="edit-button">Edit Section</button>
                <button @click="deleteSection(section.id)" class="delete-button">Delete Section</button>
            </div>
        </div>
    </div>
</template>

<style scoped>
.sections-and-products-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 5px;
}

.section-container {
    margin-bottom: 20px;
    color: black;
}

h3 {
    margin-bottom: 10px;
    color: #ddd;
}

.products-list {
    list-style: none;
    padding: 0;
}

.product-item {
    padding: 10px;
    background-color: #f9f9f9;
    border: 1px solid #ddd;
    border-radius: 3px;
    margin-bottom: 5px;
}

.section-buttons {
    display: flex;
    gap: 10px;
}

.edit-button,
.delete-button {
    background-color: #3498db;
    color: white;
    padding: 8px 12px;
    border: none;
    border-radius: 3px;
    cursor: pointer;
}

.edit-button:hover,
.delete-button:hover {
    background-color: #2980b9;
}
</style>

<script>
import axios from "axios";

export default {
    data() {
        return {
            sections: [],
        };
    },
    mounted() {
        this.fetchSections(); // Fetch sections when the component is mounted
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
        editSection(section_id) {
            this.$router.push(`/edit-section/${section_id}`);
        },
        deleteSection(section_id) {
            if (confirm("Are you sure you want to delete this section?")) {
                const jwtToken = localStorage.getItem("access_token");

                const config = {
                    headers: {
                        Authorization: `Bearer ${jwtToken}`,
                    },
                };

                axios
                    .delete(`/api/sections/${section_id}`, config)
                    .then(() => {
                        // Section deleted successfully, now refresh the sections
                        this.fetchSections(); // Fetch sections again to refresh the view
                    })
                    .catch((error) => {
                        console.error("Failed to delete section:", error);
                    });
            }
        },
    },
};
</script>
