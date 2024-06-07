<template>
    <div class="edit-section-container">
        <h2>Edit Section</h2>
        <form @submit.prevent="updateSection" class="edit-section-form">
            <div class="form-group">
                <label for="sectionName">Section Name:</label>
                <input type="text" id="sectionName" v-model="sectionName" required>
            </div>
            <div class="form-group">
                <button type="submit" class="update-button">Update Section</button>
            </div>
        </form>
    </div>
</template>

<style scoped>
.edit-section-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 5px;
}

h2 {
    margin-bottom: 20px;
}

.edit-section-form {
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

input {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
}

.update-button {
    background-color: #3498db;
    color: white;
    padding: 10px;
    border: none;
    border-radius: 3px;
    cursor: pointer;
}

.update-button:hover {
    background-color: #2980b9;
}
</style>


<script>
import axios from "axios";

export default {
    data() {
        return {
            sectionName: "", // Initialize with an empty string
        };
    },
    created() {
        // Fetch the current section data from the API and populate the sectionName
        this.fetchSectionData(); // Implement the fetchSectionData method
    },
    methods: {
        fetchSectionData() {
            // Fetch the section data from the API based on the route parameter (sectionId)
            const sectionId = this.$route.params.sectionId;
            axios.get(`/api/sections/${sectionId}`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("access_token")}`,
                },
            })
                .then((response) => {
                    this.sectionName = response.data.name;
                })
                .catch((error) => {
                    console.error("Failed to fetch section data:", error);
                });
        },
        updateSection() {
            const sectionId = this.$route.params.sectionId;
            const jwtToken = localStorage.getItem("access_token");
            const config = {
                headers: {
                    Authorization: `Bearer ${jwtToken}`,
                },
            };
            const data = {
                name: this.sectionName,
            };
            axios
                .put(`/api/sections/${sectionId}`, data, config)
                .then(() => {
                    // Section updated successfully, you can handle the response here
                    console.log("Section updated");
                    this.$router.push("/sections"); // Redirect to the sections list page
                })
                .catch((error) => {
                    console.error("Failed to update section:", error);
                });
        },
    },
};
</script>
