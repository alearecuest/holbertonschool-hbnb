console.log('✅ scripts.js loaded');
document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  const errorDiv  = document.getElementById('login-error');

  if (loginForm) {
    loginForm.addEventListener('submit', async event => {
      event.preventDefault();
      errorDiv.textContent = '';

      const email    = loginForm.email.value.trim();
      const password = loginForm.password.value.trim();

      if (!email || !password) {
        errorDiv.textContent = 'Email and password are required';
        return;
      }

      await loginUser(email, password, errorDiv);
    });
  }
});

async function loginUser(email, password, errorDiv) {
  try {
    const response = await fetch('/api/v1/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ email, password })
    });

    if (response.ok) {
      const { access_token: token } = await response.json();
      setTokenCookie(token);
      window.location.href = '/';
    } else {
      let message = response.statusText;
      try {
        const errData = await response.json();
        if (errData.message) message = errData.message;
      } catch {}
      errorDiv.textContent = `Login failed: ${message}`;
    }
  } catch {
    errorDiv.textContent = 'Error connecting to the server';
  }
}

function setTokenCookie(token) {
  const days    = 1;
  const expires = new Date(Date.now() + days * 864e5).toUTCString();
  document.cookie = `token=${token}; expires=${expires}; path=/`;
}
