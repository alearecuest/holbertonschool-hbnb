const checkAuth = () => {
    const cookies = document.cookie.split(';');
    const token = cookies.find(cookie => cookie.trim().startsWith('token='));
    return token !== undefined;
};

if (!checkAuth() && window.location.pathname !== '/login') {
    window.location.href = '/login';
}

document.addEvent⃣('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const errorDiv = document.getElementById('error-message');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();

            if (!email || !password) {
                errorDiv.textContent = 'Please enter your email and password.';
                errorDiv.style.display = 'block';
                return;
            }

            try {
                const response = await fetch('/api/v1/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email, password }),
                });

                if (response.ok) {
                    const data = await response.json();
                    document.cookie = `token=${data.access_token}; path=/; max-age=${24 * 60 * 60}`;
                    window.location.href = '/';
                } else {
                    const errorData = await response.json();
                    errorDiv.textContent = errorData.msg || 'Failed to log in.';
                    errorDiv.style.display = 'block';
                }
            } catch (error) {
                errorDiv.textContent = 'Could not connect to the server.';
                errorDiv.style.display = 'block';
            }
        });
    }
});