document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('register-form');
    if (!form) return;

    form.addEventListener('submit', async function (event) {
        event.preventDefault();
        const user = {
            username: document.getElementById('username').value.trim(),
            email: document.getElementById('email').value.trim(),
            first_name: document.getElementById('first_name').value.trim(),
            last_name: document.getElementById('last_name').value.trim(),
            phone_number: document.getElementById('phone_number').value.trim(),
            role: document.getElementById('role').value.trim(),
            password: document.getElementById('password').value.trim(),
        };
        const errorEl = document.getElementById('register-error');
        const successEl = document.getElementById('register-success');
        errorEl.textContent = '';
        successEl.textContent = '';

        try {
            await fetchJson('/auth/', {
                method: 'POST',
                headers: authHeaders(),
                body: JSON.stringify(user),
            });
            successEl.textContent = 'Account created successfully. Redirecting to login...';
            setTimeout(() => {
                window.location.href = '/login';
            }, 1200);
        } catch (error) {
            errorEl.textContent = error.detail || 'Registration failed. Please try again.';
        }
    });
});
