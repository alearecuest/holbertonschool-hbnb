document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('register-form');
    const errorMessage = document.getElementById('error-message');

    registerForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        errorMessage.style.display = 'none';

        const first_name = document.getElementById('first_name').value.trim();
        const last_name = document.getElementById('last_name').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value.trim();

        if (!first_name || !last_name || !email || !password) {
            errorMessage.textContent = 'All fields are required';
            errorMessage.style.display = 'block';
            return;
        }

        if (password.length < 6) {
            errorMessage.textContent = 'Password must be at least 6 characters long';
            errorMessage.style.display = 'block';
            return;
        }

        try {
            const response = await fetch('/api/v1/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    first_name,
                    last_name,
                    email,
                    password
                })
            });

            const data = await response.json();

            if (response.ok) {
                window.location.href = '/login?registered=true';
            } else {
                errorMessage.textContent = data.msg || 'Registration failed';
                errorMessage.style.display = 'block';
            }
        } catch (error) {
            console.error('Error during registration:', error);
            errorMessage.textContent = 'Network error. Please try again later.';
            errorMessage.style.display = 'block';
        }
    });
});