// utils/auth.js

// Function to check if the user is authenticated
export function isAuthenticated() {
  // Check if a valid token exists in localStorage or sessionStorage
  const token = localStorage.getItem('access_token') || sessionStorage.getItem('access_token');
  return token !== null && token !== undefined;
}

// Function to get the user role from the stored token
export function getUserRole() {
  // Retrieve user role from localStorage or sessionStorage
  const token = localStorage.getItem('access_token') || sessionStorage.getItem('access_token');
  
  if (token) {
    // Decode the JWT token and extract the user role
    const decodedToken = atob(token.split('.')[1]);
    const { role } = JSON.parse(decodedToken);
    return role;
  }

  // If no role is found, return a default role or handle it as needed
  return null;
}
