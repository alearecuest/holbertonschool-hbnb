// app/static/js/scripts.js

/**
 * Safely read a cookie by name.
 */
function getCookie(name) {
  const pairs = document.cookie.split(/;\s*/);
  for (let pair of pairs) {
    const [key, ...vals] = pair.split('=');
    if (key === name) return vals.join('=');
  }
  return null;
}

async function fetchPlaces(token) {
  try {
    const res = await fetch('/api/v1/places', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    if (!res.ok) return console.error('Failed to fetch places');
    const places = await res.json();
    displayPlaces(places);
  } catch (err) {
    console.error('Error fetching places:', err);
  }
}

function displayPlaces(places) {
  const container = document.getElementById('places-list');
  container.innerHTML = '';
  places.forEach(place => {
    const div = document.createElement('div');
    div.className = 'place-card';
    div.dataset.price = place.price;
    div.innerHTML = `
      <h3>${place.title || 'Unnamed Property'}</h3>
      <p>${place.description || 'No description'}</p>
      <p>Price: $${place.price}</p>
      <button class="details-button">View Details</button>
    `;
    container.appendChild(div);
  });
}

function applyPriceFilter() {
  const max = document.getElementById('price-filter').value;
  const maxPrice = max === 'All' ? Infinity : +max;
  document.querySelectorAll('.place-card').forEach(c => {
    c.style.display = (+c.dataset.price <= maxPrice ? 'block' : 'none');
  });
}

document.addEventListener('DOMContentLoaded', () => {
  const token     = getCookie('token');
  const loginLink = document.getElementById('login-link');

  // 1) Redirigir a /login si no estamos autenticados y no estamos ya en /login
  if (!token && window.location.pathname !== '/login') {
    window.location.replace('/login');
    return;
  }

  // 2) Mostrar siempre el enlace Login
  if (loginLink) loginLink.style.display = 'block';

  // 3) Si hay token, cargar propiedades
  if (token) {
    fetchPlaces(token);
  }

  // 4) Vincular filtro de precio
  const priceFilter = document.getElementById('price-filter');
  if (priceFilter) {
    priceFilter.addEventListener('change', applyPriceFilter);
  }

  // 5) Lógica de login en /login
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    const errorDiv = document.getElementById('error-message');
    loginForm.addEventListener('submit', async e => {
      e.preventDefault();
      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value.trim();

      if (!email || !password) {
        errorDiv.textContent = 'Please, enter mail and password.';
        errorDiv.style.display = 'block';
        return;
      }
      try {
        const res = await fetch('/api/v1/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });
        const body = await res.json();
        if (!res.ok) {
          errorDiv.textContent = body.msg || 'Login error.';
          errorDiv.style.display = 'block';
          return;
        }
        document.cookie = `token=${body.access_token}; path=/; max-age=${24*60*60}`;
        window.location.replace('/');
      } catch {
        errorDiv.textContent = 'Could not connect to the server.';
        errorDiv.style.display = 'block';
      }
    });
  }
});
