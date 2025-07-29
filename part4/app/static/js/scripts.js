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

  const filterSelect = document.getElementById('price-filter');
  if (filterSelect) {
    filterSelect.addEventListener('change', filterPlaces);
  }

  checkAuthentication();
});

function getCookie(name) {
  const cookies = document.cookie.split('; ').map(c => c.split('='));
  const match   = cookies.find(pair => pair[0] === name);
  return match ? decodeURIComponent(match[1]) : null;
}

function checkAuthentication() {
  const token     = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (!loginLink) return;

  if (!token) {
    loginLink.style.display = 'block';
  } else {
    loginLink.style.display = 'none';
    fetchPlaces(token);
  }
}

async function fetchPlaces(token) {
  try {
    const res = await fetch('/api/v1/places', {
      headers: token
        ? { 'Authorization': `Bearer ${token}` }
        : {}
    });

    if (res.ok) {
      const places = await res.json();
      displayPlaces(places);
    } else {
      console.error('Failed to fetch places:', res.status, res.statusText);
    }
  } catch (err) {
    console.error('Error fetching places:', err);
  }
}

function displayPlaces(places) {
  const container = document.getElementById('places-list');
  if (!container) return;
  container.innerHTML = '';

  places.forEach(place => {
    const card = document.createElement('div');
    card.className = 'place-card';
    card.setAttribute('data-price', place.price);

    card.innerHTML = `
      <h2>${place.name}</h2>
      <p>${place.description}</p>
      <p>Location: ${place.city}, ${place.state}</p>
      <p>Price: $${place.price} per night</p>
      <button
        class="details-button"
        onclick="location.href='/place'"
      >
        View Details
      </button>
    `;
    container.appendChild(card);
  });
}

function filterPlaces(event) {
  const maxPrice = event.target.value;
  document.querySelectorAll('.place-card').forEach(card => {
    const price = parseFloat(card.getAttribute('data-price'));
    card.style.display =
      maxPrice === 'All' || price <= parseFloat(maxPrice)
        ? ''
        : 'none';
  });
}

async function loginUser(email, password, errorDiv) {
  try {
    const res = await fetch('/api/v1/auth/login', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ email, password })
    });

    if (res.ok) {
      const { access_token: token } = await res.json();
      setTokenCookie(token);
      window.location.href = '/';
    } else {
      let msg = res.statusText;
      try {
        const errData = await res.json();
        if (errData.message) msg = errData.message;
      } catch {}
      errorDiv.textContent = `Login failed: ${msg}`;
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
