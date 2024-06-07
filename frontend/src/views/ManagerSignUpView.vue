<template>
    <div class="signup-container">
        <h2>Manager Sign Up</h2>
        <form @submit.prevent="signup" class="signup-form">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" v-model="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="password" required>
            </div>
            <div class="form-group">
                <label for="retypePassword">Retype Password:</label>
                <input type="password" id="retypePassword" v-model="retypePassword" required>
            </div>
            <div class="form-group">
                <button type="submit">Sign Up</button>
            </div>
        </form>
        <p v-if="message" class="success-message">{{ message }}</p>
    </div>
</template>

<script>
import axios from "axios";
export default {
    data() {
        return {
            username: '',
            password: '',
            retypePassword: '',
            message: ''
        };
    },
    methods: {
        async signup() {
            if (this.password !== this.retypePassword) {
                this.message = 'Passwords do not match.';
                return;
            }

            try {
                const response = await axios.post('/signup/manager', {
                    username: this.username,
                    password: this.password
                });

                if (response.status === 200) {
                    this.message = 'Account created. Account will be activated after admin approval... Redirecting to login...';
                    setTimeout(() => {
                        this.$router.push('/manager/login'); 
                    }, 3000);  
                }
            } catch (error) {
                console.log(error);
                this.message = 'Failed to sign up. Please try again.';
            }
        }
    }
};
</script>

<style scoped>
.signup-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 5px;
}

.signup-form {
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

.success-message {
    color: #2ecc71;
    margin-top: 10px;
}
</style>
