document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('login-form');
    if (!form) return;

    form.addEventListener('submit', async function (event) {
        event.preventDefault();
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value.trim();
        const errorEl = document.getElementById('login-error');
        errorEl.textContent = '';

        try {
            const body = new URLSearchParams();
            body.append('username', username);
            body.append('password', password);
            const response = await fetchJson('/auth/token', {
                method: 'POST',
                headers: authHeaders('application/x-www-form-urlencoded'),
                body: body.toString(),
            });
            setAuthToken(response.access_token);
            window.location.href = '/todos';
        } catch (error) {
            errorEl.textContent = error.detail || 'Login failed. Check your credentials.';
        }
    });
});
