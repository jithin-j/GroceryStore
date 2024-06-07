<template>
    <div class="manager-login-container">
        <h2>Manager Login</h2>
        <form @submit.prevent="login" class="login-form">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" v-model="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="password" required>
            </div>
            <div class="form-group">
                <button type="submit">Log In</button>
            </div>
        </form>
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </div>
</template>

<script>
import axios from "axios";
export default {
    data() {
        return {
            username: '',
            password: '',
            errorMessage: ''
        };
    },
    methods: {
        async login() {

            try {
                const response = await axios.post('/manager/login', {
                    username: this.username,
                    password: this.password
                });
                if (response.status === 200) {
                    // Store the access token in local storage
                    localStorage.setItem('access_token', response.data.access_token);
                    // Redirect to the dashboard page
                    this.$router.push('/manager/dashboard');
                }
            } catch (error) {
                if (error.response && error.response.status === 401) {
                    if (error.response.data.message === "Account pending admin approval") {
                        this.errorMessage = 'Login failed. Account pending admin approval.';
                        console.log(this.errorMessage);
                    } else {
                        this.errorMessage = 'Login failed. Please check your credentials.';
                    }
                } else {
                    // Handle other errors (e.g., network issues, server errors)
                    this.errorMessage = 'An error occurred while processing your request.';
                }
            }
        }
    }
};
</script>

<style scoped>
.manager-login-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 5px;
}

.login-form {
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
