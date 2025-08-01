function getCookie(name) {
  const cookieArr = document.cookie.split(';').map(c => c.trim());
  for (let cookie of cookieArr) {
    if (cookie.startsWith(name + '=')) {
      return decodeURIComponent(cookie.split('=')[1]);
    }
  }
  return null;
}

function setCookie(name, value, days) {
  const d = new Date();
  d.setTime(d.getTime() + days * 24 * 60 * 60 * 1000);
  document.cookie = `${name}=${encodeURIComponent(value)};path=/;expires=${d.toUTCString()}`;
}

function deleteCookie(name) {
  document.cookie = `${name}=; Max-Age=0; path=/;`;
}

function checkAuthentication() {
  const token = getCookie('token');
  if (!token) {
    window.location.href = 'index.html';
  }
  return token;
}

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('place_id');
}

async function handleLogin(event) {
  event.preventDefault();
  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value.trim();

  try {
    const res = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });

    if (res.ok) {
      const data = await res.json();
      setCookie('token', data.token, 7);
      window.location.href = 'index.html';
    } else {
      const err = await res.json().catch(() => ({}));
      alert(err.message || 'Login failed');
    }
  } catch (err) {
    console.error(err);
    alert('Network error during login');
  }
}

function handleLogout() {
  deleteCookie('token');
  window.location.href = 'index.html';
}

async function fetchPlaces() {
  try {
    const res = await fetch('/api/places');
    if (!res.ok) throw new Error('Failed to load places');
    const places = await res.json();
    displayPlaces(places);
  } catch (err) {
    console.error(err);
    document.getElementById('places-list').innerText = 'Error loading places';
  }
}

function displayPlaces(places) {
  const container = document.getElementById('places-list');
  container.innerHTML = '';

  places.forEach(place => {
    const card = document.createElement('div');
    card.className = 'place-card';
    card.innerHTML = `
      <img src="${place.image_url}" alt="${place.name}" />
      <h2>${place.name}</h2>
      <p>${place.description}</p>
      <p>Price: $${place.price}</p>
      <a href="add_review.html?place_id=${place.id}" class="button">Add Review</a>
    `;
    container.appendChild(card);
  });
}

async function submitNewPlace(event) {
  event.preventDefault();
  const token = checkAuthentication();

  const name = document.getElementById('name').value.trim();
  const address = document.getElementById('address').value.trim();
  const price = parseFloat(document.getElementById('price').value);
  const description = document.getElementById('description').value.trim();
  const imageUrl = document.getElementById('image_url').value.trim();

  try {
    const res = await fetch('/api/places', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ name, address, price, description, image_url: imageUrl })
    });

    if (res.ok) {
      alert('Place created successfully');
      window.location.href = 'index.html';
    } else {
      const err = await res.json().catch(() => ({}));
      alert(err.message || 'Failed to create place');
    }
  } catch (err) {
    console.error(err);
    alert('Network error submitting place');
  }
}

async function submitReview(token, placeId, comment, rating) {
  const endpoint = `/api/places/${placeId}/reviews`;
  const res = await fetch(endpoint, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ comment, rating })
  });
  return res;
}

async function handleReviewResponse(response) {
  if (response.ok) {
    alert('Review submitted successfully!');
    document.getElementById('comment').value = '';
    document.getElementById('rating').value = '';
  } else {
    const err = await response.json().catch(() => ({}));
    alert(err.message || 'Failed to submit review');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', handleLogin);
  }

  const logoutBtn = document.getElementById('logout-button');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', handleLogout);
  }

  const placesList = document.getElementById('places-list');
  if (placesList) {
    fetchPlaces();
  }

  const addPlaceForm = document.getElementById('add-place-form');
  if (addPlaceForm) {
    addPlaceForm.addEventListener('submit', submitNewPlace);
  }

  const reviewForm = document.querySelector('.add-review form');
  if (reviewForm) {
    const token = checkAuthentication();
    const placeId = getPlaceIdFromURL();
    if (!placeId) {
      alert('Place ID missing in URL');
      window.location.href = 'index.html';
      return;
    }

    reviewForm.addEventListener('submit', async event => {
      event.preventDefault();
      const comment = document.getElementById('comment').value.trim();
      const rating = parseInt(document.getElementById('rating').value, 10);

      if (!comment) {
        alert('Please enter your comment.');
        return;
      }

      try {
        const res = await submitReview(token, placeId, comment, rating);
        await handleReviewResponse(res);
      } catch (err) {
        console.error(err);
        alert('Network error submitting review');
      }
    });
  }
});
