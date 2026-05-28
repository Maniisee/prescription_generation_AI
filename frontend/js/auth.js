// Authentication helper functions

// Check if user is authenticated, redirect to login if not
function checkAuth() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'login.html';
        return false;
    }
    return true;
}

// Verify token with server
async function verifyToken() {
    const token = localStorage.getItem('token');
    if (!token) return false;

    try {
        const response = await fetch(`${API_URL}/api/auth/verify`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            // Token invalid or expired
            localStorage.clear();
            window.location.href = 'login.html';
            return false;
        }

        return true;
    } catch (error) {
        console.error('Token verification error:', error);
        return false;
    }
}

// Logout function
function logout() {
    localStorage.clear();
    window.location.href = 'index.html';
}

// Get current user data
function getCurrentUserData() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}
