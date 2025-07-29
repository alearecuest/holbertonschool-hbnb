function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

function getCookie(name) {
  const match = document.cookie.match(
    new RegExp('(?:^|; )' + name.replace(/([.$?*|{}()[]\\/+^])/g, '\\$1') + '=([^;]*)')
  );
  return match ? decodeURIComponent(match[1]) : null;
}

async function fetchPlaceDetails(token, placeId) {
  const headers = {};
  if (token) {
    headers['Authorization'] = 'Bearer ' + token;
  }

  try {
    const response = await fetch(`/api/v1/places/${placeId}`, { headers });
    if (!response.ok) {
      throw new Error('Failed to fetch place details');
    }
    const place = await response.json();
    displayPlaceDetails(place);
  } catch (err) {
    console.error('Error loading place details:', err);
  }
}

function displayPlaceDetails(place) {
  const container = document.getElementById('place-details');
  container.innerHTML = ''; // Clear previous content

  const titleEl = document.createElement('h2');
  titleEl.textContent = place.name;
  container.appendChild(titleEl);

  const descEl = document.createElement('p');
  descEl.textContent = place.description;
  container.appendChild(descEl);

  const priceEl = document.createElement('p');
  priceEl.textContent = `Price per night: $${place.price}`;
  container.appendChild(priceEl);

  if (place.amenities && place.amenities.length) {
    const amenTitle = document.createElement('h3');
    amenTitle.textContent = 'Amenities:';
    container.appendChild(amenTitle);

    const ul = document.createElement('ul');
    place.amenities.forEach(amenity => {
      const li = document.createElement('li');
      li.textContent = amenity.name;
      ul.appendChild(li);
    });
    container.appendChild(ul);
  }

  const revTitle = document.createElement('h3');
  revTitle.textContent = 'Reviews:';
  container.appendChild(revTitle);

  if (place.reviews && place.reviews.length) {
    place.reviews.forEach(review => {
      const div = document.createElement('div');
      div.className = 'review';

      const author = document.createElement('strong');
      author.textContent =
        review.user_name || `${review.user.first_name} ${review.user.last_name}`;
      div.appendChild(author);

      const text = document.createElement('p');
      text.textContent = review.text;
      div.appendChild(text);

      const score = document.createElement('p');
      score.textContent = `Rating: ${review.rating}`;
      div.appendChild(score);

      container.appendChild(div);
    });
  } else {
    const none = document.createElement('p');
    none.textContent = 'No reviews yet.';
    container.appendChild(none);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const placeId = getPlaceIdFromURL();
  if (!placeId) {
    console.error('Missing place ID in URL');
    return;
  }

  const token = getCookie('token');
  const addReviewSection = document.getElementById('add-review');

  if (token) {
    addReviewSection.style.display = 'block';
  } else {
    addReviewSection.style.display = 'none';
  }

  fetchPlaceDetails(token, placeId);

  document.getElementById('review-form').addEventListener('submit', async e => {
    e.preventDefault();
    const text = document.getElementById('review-text').value.trim();
    const rating = +document.getElementById('review-rating').value;

    try {
      const res = await fetch(`/api/v1/places/${placeId}/reviews`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + token
        },
        body: JSON.stringify({ text, rating })
      });

      if (!res.ok) {
        throw new Error('Failed to submit review');
      }

      fetchPlaceDetails(token, placeId);
      e.target.reset();
    } catch (err) {
      console.error(err);
    }
  });
});
