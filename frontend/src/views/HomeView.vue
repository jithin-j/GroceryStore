<script setup>
import { RouterLink } from 'vue-router';
</script>

<template>
  <main class="landing-page">
    <h1 class="heading">Welcome to the Grocery Store App</h1>
    <div class="cta-buttons">
      <RouterLink to="/login" class="cta-button login-button">Login</RouterLink>
      <RouterLink to="/signup" class="cta-button signup-button">Sign Up</RouterLink>
    </div>
  </main>
</template>

<style scoped>
.landing-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 80vh;
  background-color: #dddedd;
}

.heading {
  font-size: 2.5em;
  margin-bottom: 20px;
  color: #343a40;
  /* Dark gray text color */
}

.cta-buttons {
  display: flex;
  gap: 20px;
}

.cta-button {
  padding: 15px 30px;
  font-size: 1.2em;
  text-align: center;
  text-decoration: none;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.login-button {
  background-color: #007bff;
  /* Blue color */
}

.signup-button {
  background-color: #28a745;
  /* Green color */
}

.cta-button:hover {
  opacity: 0.9;
}</style>
