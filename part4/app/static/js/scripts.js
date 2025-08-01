;(function () {
  function getCookie(name) {
    return document.cookie
      .split(';')
      .map(c => c.trim())
      .find(c => c.startsWith(name + '='))
      ?.split('=')[1] || null;
  }

  async function fetchPlaces(token) {
    try {
      const res = await fetch('/api/v1/places', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      if (!res.ok) throw new Error(`Failed to fetch places (${res.status})`);
      const places = await res.json();
      displayPlaces(places);
    } catch (err) {
      console.error('Error fetching places:', err);
    }
  }

  function displayPlaces(places) {
    const container = document.getElementById('places-list');
    container.innerHTML = '';
    if (places.length === 0) {
      container.textContent = 'No properties available.';
      return;
    }
    places.forEach(place => {
      const div = document.createElement('div');
      div.className = 'place-card';
      div.dataset.price = place.price;
      div.innerHTML = `
        <h3>${place.title || 'Unnamed Property'}</h3>
        <p>${place.description || 'No description'}</p>
        <p>Price: $${place.price.toFixed(2)}</p>
        <button class="details-button"
                onclick="window.location.href='/place.html?id=${place.id}'">
          View Details
        </button>
      `;
      container.appendChild(div);
    });
  }

  function applyPriceFilter() {
    const maxValue = document.getElementById('price-filter').value;
    const maxPrice = maxValue === 'All' ? Infinity : +maxValue;
    document.querySelectorAll('.place-card').forEach(card => {
      const price = +card.dataset.price;
      card.style.display = price <= maxPrice ? 'block' : 'none';
    });
  }

  async function fetchPlaceDetails(placeId, token) {
    try {
      const headers = token
        ? { 'Authorization': `Bearer ${token}` }
        : {};
      const resp = await fetch(`/api/v1/places/${placeId}`, { headers });
      if (!resp.ok) throw new Error(`Error ${resp.status} getting details`);
      const place = await resp.json();
      displayPlaceDetails(place);
    } catch (err) {
      console.error(err);
      document.getElementById('place-details')
        .textContent = 'The details could not be loaded.';
    }
  }

  function displayPlaceDetails(place) {
    const c = document.getElementById('place-details');
    c.innerHTML = '';

    const title = document.createElement('h2');
    title.textContent = place.title;
    const desc = document.createElement('p');
    desc.textContent = place.description || '';
    const price = document.createElement('p');
    price.textContent = `Price per night: $${place.price.toFixed(2)}`;

    const amenTitle = document.createElement('h4');
    amenTitle.textContent = 'Amenities';
    const amenList = document.createElement('ul');
    place.amenities.forEach(a => {
      const li = document.createElement('li');
      li.textContent = `${a.name} (${a.id})`;
      amenList.appendChild(li);
    });

    const revSection = document.createElement('section');
    const revTitle = document.createElement('h4');
    revTitle.textContent = 'Reviews';
    revSection.appendChild(revTitle);

    if (!place.reviews || place.reviews.length === 0) {
      const noRev = document.createElement('p');
      noRev.textContent = 'There are no reviews yet.';
      revSection.appendChild(noRev);
    } else {
      place.reviews.forEach(r => {
        const div = document.createElement('div');
        div.className = 'review';
        div.innerHTML = `
          <strong>${r.user.first_name} ${r.user.last_name}</strong>
          <p>Rating: ${r.rating} / 5</p>
          <p>${r.text}</p>
        `;
        revSection.appendChild(div);
      });
    }

    c.append(title, desc, price, amenTitle, amenList, revSection);
  }

  async function submitReview(placeId, token) {
    const text = document.getElementById('review-text').value.trim();
    const rating = +document.getElementById('review-rating').value || 0;
    if (!text || rating < 1 || rating > 5) return;

    try {
      const resp = await fetch(
        `/api/v1/places/${placeId}/reviews`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({ text, rating })
        }
      );
      if (!resp.ok) throw new Error(`Sending failed (${resp.status})`);
      document.getElementById('review-text').value = '';
      document.getElementById('review-rating').value = '';
      await fetchPlaceDetails(placeId, token);
    } catch (err) {
      console.error(err);
      alert('Error submitting review.');
    }
  }

  function toggleReviewForm(token, placeId) {
    const formSection = document.getElementById('add-review');
    if (!formSection) return;
    if (token) {
      formSection.style.display = 'block';
      const form = document.getElementById('review-form');
      form.addEventListener('submit', e => {
        e.preventDefault();
        submitReview(placeId, token);
      });
    } else {
      formSection.style.display = 'none';
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token && window.location.pathname !== '/login') {
      window.location.replace('/login');
      return;
    }
    if (loginLink) loginLink.style.display = 'block';

    if (document.getElementById('places-list')) {
      if (token) fetchPlaces(token);
      const priceFilter = document.getElementById('price-filter');
      if (priceFilter) priceFilter.addEventListener('change', applyPriceFilter);
    }

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
      const errorDiv = document.getElementById('error-message');
      loginForm.addEventListener('submit', async e => {
        e.preventDefault();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value.trim();
        if (!email || !password) {
          errorDiv.textContent = 'Please enter email and password.';
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

    if (document.getElementById('place-details')) {
      const params = new URLSearchParams(window.location.search);
      const placeId = params.get('id');
      toggleReviewForm(token, placeId);
      fetchPlaceDetails(placeId, token);
    }
  });
})();
