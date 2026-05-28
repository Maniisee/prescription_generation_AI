// API Configuration
// Using 127.0.0.1 instead of localhost to force IPv4
// (Flask backend only listens on IPv4, browsers try IPv6 first with localhost)
const API_URL = 'http://127.0.0.1:5001';

// Helper function for authenticated API requests
function getAuthHeaders() {
    const token = localStorage.getItem('token');
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    };
}

// Helper function to check if user is authenticated
function isAuthenticated() {
    return !!localStorage.getItem('token');
}

// Helper function to get current user
function getCurrentUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}
