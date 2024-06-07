<template>
    <div class="create-request-container">
        <form @submit.prevent="submitSectionRequest" class="create-request-form">
            <h2>Create a request for new section</h2>
            <div class="form-group">
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
.create-request-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 5px;
}

.create-request-form {
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
            requestType: "create",
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
