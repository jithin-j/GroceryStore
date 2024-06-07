<template>
    <div class="add-section-container">
        <h2>Add New Section</h2>
        <form @submit.prevent="addSection" class="add-section-form">
            <div class="form-group">
                <label for="sectionName">Section Name:</label>
                <input type="text" id="sectionName" v-model="sectionName" required>
            </div>
            <div class="form-group">
                <button type="submit" class="add-button">Add Section</button>
            </div>
        </form>
    </div>
</template>

<style scoped>
.add-section-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 5px;
}

h2 {
    margin-bottom: 20px;
}

.add-section-form {
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

.add-button {
    background-color: #2ecc71;
    color: white;
    padding: 10px;
    border: none;
    border-radius: 3px;
    cursor: pointer;
}

.add-button:hover {
    background-color: #27ae60;
}
</style>


<script>
import axios from "axios";

export default {
    data() {
        return {
            sectionName: "",
        };
    },
    methods: {
        addSection() {
            // Get the JWT token from local storage
            const jwtToken = localStorage.getItem("access_token");

            // Set the authorization header with the JWT token
            const config = {
                headers: {
                    Authorization: `Bearer ${jwtToken}`,
                },
            };

            // Create the payload
            const data = { name: this.sectionName };

            // Make the POST request with the token and data
            axios
                .post("/api/sections/add", data, config)
                .then((response) => {
                    // Section added successfully, you can handle the response here
                    console.log("Section added:", response.data);
                    // Optionally, you can navigate to another page after adding the section
                    this.$router.push("/sections");
                })
                .catch((error) => {
                    console.error("Failed to add section:", error);
                });
        },
    },
};
</script>
