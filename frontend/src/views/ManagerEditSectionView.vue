<template>
    <div class="edit-section-container">
        <h2>Edit or Delete Section</h2>
        <form @submit.prevent="submitSectionRequest" class="edit-section-form">
            <div class="form-group">
                <label for="requestType">Request Type:</label>
                <select id="requestType" v-model="requestType" required>
                    <option value="edit">Edit</option>
                    <option value="delete">Delete</option>
                </select>
            </div>
            <div v-if="requestType === 'edit'" class="form-group">
                <label for="sectionName">New Section Name:</label>
                <input type="text" id="sectionName" v-model="sectionName" required>
            </div>
            <div class="form-group">
                <button type="submit">Submit Request</button>
            </div>
        </form>
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
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
            requestType: "edit",
            sectionName: "",
            errorMessage: "",
        };
    },
    methods: {
        submitSectionRequest() {
            const jwtToken = localStorage.getItem("access_token");

            // Decode the JWT to access claims (including user ID)
            const sectionId = this.$route.params.sectionId;

            const data = {
                request_type: this.requestType,
                section_id: sectionId,
                section_name: this.sectionName,
            };

            const config = {
                headers: {
                    Authorization: `Bearer ${jwtToken}`,
                },
            };

            axios
                .post("/api/section-requests", data, config)
                .then(() => {
                    console.log("Section request submitted successfully");
                    this.$router.push("/manager/dashboard");
                })
                .catch((error) => {
                    console.error("Failed to submit section request:", error);
                    this.errorMessage = "Failed to submit section request. Please check your data.";
                });
        },
    },
};
</script>
