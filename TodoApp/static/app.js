function getAuthToken() {
    return localStorage.getItem('todoToken');
}

function setAuthToken(token) {
    localStorage.setItem('todoToken', token);
}

function clearAuthToken() {
    localStorage.removeItem('todoToken');
}

function authHeaders(contentType = 'application/json') {
    const headers = { 'Content-Type': contentType };
    const token = getAuthToken();
    if (token) {
        headers.Authorization = `Bearer ${token}`;
    }
    return headers;
}

function updateNav() {
    const navLinks = document.getElementById('nav-links');
    if (!navLinks) {
        return;
    }
    if (getAuthToken()) {
        navLinks.innerHTML = '<a href="/todos">My Todos</a> <a href="#" id="logout-link">Logout</a>';
        const logoutLink = document.getElementById('logout-link');
        if (logoutLink) {
            logoutLink.addEventListener('click', function (event) {
                event.preventDefault();
                clearAuthToken();
                window.location.href = '/login';
            });
        }
    } else {
        navLinks.innerHTML = '<a href="/login">Login</a> <a href="/register">Register</a>';
    }
}

document.addEventListener('DOMContentLoaded', updateNav);

async function fetchJson(url, options = {}) {
    const response = await fetch(url, options);
    const text = await response.text();
    let data;
    try {
        data = JSON.parse(text);
    } catch (e) {
        data = { detail: text };
    }
    if (!response.ok) {
        throw data;
    }
    return data;
}

function requireAuth() {
    if (!getAuthToken()) {
        window.location.href = '/login';
        return false;
    }
    return true;
}
