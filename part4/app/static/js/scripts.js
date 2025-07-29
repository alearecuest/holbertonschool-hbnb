function getCookie(name) {
  const re = new RegExp('(^|; )' +
    name.replace(/([.$?*|{}()[]\\/+^])/g, '\\$1') +
    '=([^;]+)');
  const match = document.cookie.match(re);
  return match ? decodeURIComponent(match[2]) : null;
}

function checkAuthentication() {
  const token = getCookie('token');
  if (!token) {
    window.location.href = '/';
    return null;
  }
  return token;
}

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

async function fetchPlaceDetails(token, placeId) {
  const headers = token
    ? { 'Authorization': 'Bearer ' + token }
    : {};
  try {
    const res = await fetch(`/api/v1/places/${placeId}`, { headers });
    if (!res.ok) throw new Error('Failed to fetch place details');
    const place = await res.json();
    displayPlaceDetails(place);
  } catch (err) {
    console.error(err);
    document.getElementById('place-details')
            .textContent = 'Error loading place details.';
  }
}

function displayPlaceDetails(place) {
  const container = document.getElementById('place-details');
  container.innerHTML = '';

  const title = document.createElement('h2');
  title.textContent = place.name;
  container.appendChild(title);

  const desc = document.createElement('p');
  desc.textContent = place.description;
  container.appendChild(desc);

  const price = document.createElement('p');
  price.textContent = `Price per night: $${place.price}`;
  container.appendChild(price);

  if (place.amenities?.length) {
    const h3 = document.createElement('h3');
    h3.textContent = 'Amenities:';
    container.appendChild(h3);

    const ul = document.createElement('ul');
    place.amenities.forEach(a => {
      const li = document.createElement('li');
      li.textContent = a.name;
      ul.appendChild(li);
    });
    container.appendChild(ul);
  }

  const revH3 = document.createElement('h3');
  revH3.textContent = 'Reviews:';
  container.appendChild(revH3);

  if (place.reviews?.length) {
    place.reviews.forEach(r => {
      const div = document.createElement('div');
      div.className = 'review';

      const author = document.createElement('strong');
      author.textContent =
        r.user_name || `${r.user.first_name} ${r.user.last_name}`;
      div.appendChild(author);

      const textP = document.createElement('p');
      textP.textContent = r.text;
      div.appendChild(textP);

      const ratingP = document.createElement('p');
      ratingP.textContent = `Rating: ${r.rating}`;
      div.appendChild(ratingP);

      container.appendChild(div);
    });
  } else {
    const none = document.createElement('p');
    none.textContent = 'No reviews yet.';
    container.appendChild(none);
  }
}

async function submitReview(token, placeId, review) {
  return fetch(`/api/v1/places/${placeId}/reviews`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + token
    },
    body: JSON.stringify(review)
  });
}

async function handleResponse(res, token, placeId, form) {
  if (res.ok) {
    alert('Review submitted successfully!');
    form.reset();
    fetchPlaceDetails(token, placeId);
  } else if (res.status === 401) {
    alert('Session expired. Please log in again.');
    window.location.href = '/';
  } else {
    const err = await res.json().catch(() => ({}));
    alert(`Error: ${err.message || 'Unable to submit review.'}`);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const token = checkAuthentication();
  if (!token) return;

  const placeId = getPlaceIdFromURL();
  if (!placeId) {
    alert('Invalid place.');
    window.location.href = '/';
    return;
  }

  fetchPlaceDetails(token, placeId);

  const form = document.getElementById('review-form');
  form.addEventListener('submit', async e => {
    e.preventDefault();
    const rating = +document.getElementById('rating').value;
    const text = document.getElementById('comment').value.trim();

    if (!rating || !text) {
      alert('Please fill in all fields.');
      return;
    }

    const res = await submitReview(token, placeId, { rating, text });
    handleResponse(res, token, placeId, form);
  });
});
```