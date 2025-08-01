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
  const loginLink = document.getElementById('login-link');
  const logoutButton = document.getElementById('logout-button');
  
  if (loginLink && logoutButton) {
    if (token) {
      loginLink.style.display = 'none';
      logoutButton.style.display = 'block';
    } else {
      loginLink.style.display = 'block';
      logoutButton.style.display = 'none';
    }
  }
  
  return token;
}

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('place_id');
}

async function handleLogin(event) {
  event.preventDefault();
  const email = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value.trim();
  const errorMessage = document.getElementById('error-message');

  try {
    const res = await fetch('/api/v1/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    if (res.ok) {
      const data = await res.json();
      if (data.access_token) {
        setCookie('token', data.access_token, 7);
      }
      window.location.href = '/';
    } else {
      const err = await res.json().catch(() => ({}));
      if (errorMessage) {
        errorMessage.textContent = err.msg || 'Login failed';
        errorMessage.style.display = 'block';
      } else {
        alert(err.msg || 'Login failed');
      }
    }
  } catch (err) {
    console.error(err);
    if (errorMessage) {
      errorMessage.textContent = 'Network error during login';
      errorMessage.style.display = 'block';
    } else {
      alert('Network error during login');
    }
  }
}

function handleLogout(event) {
  if (event) event.preventDefault();
  deleteCookie('token');
  window.location.href = '/';
}

async function fetchPlaces() {
  try {
    const token = getCookie('token');
    const headers = {
      'Content-Type': 'application/json'
    };
    
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    
    const res = await fetch('/api/v1/places', {
      headers: headers
    });
    
    if (!res.ok) throw new Error('Failed to load places');
    const places = await res.json();
    displayPlaces(places);
    
    setupPriceFilter(places);
  } catch (err) {
    console.error(err);
    const placesList = document.getElementById('places-list');
    if (placesList) {
      placesList.innerHTML = '<p class="error">Error loading places</p>';
    }
  }
}

function displayPlaces(places) {
  const container = document.getElementById('places-list');
  if (!container) return;
  
  container.innerHTML = '';

  if (places.length === 0) {
    container.innerHTML = '<p>No places available</p>';
    return;
  }

  places.forEach(place => {
    const card = document.createElement('div');
    card.className = 'place-card';
    
    const title = place.title || place.name || 'Unnamed Place';
    const description = place.description || 'No description available';
    
    card.innerHTML = `
      <h3>${title}</h3>
      <p>${description.substring(0, 100)}${description.length > 100 ? '...' : ''}</p>
      <p class="price">Price: $${place.price}</p>
      <a href="/place?place_id=${place.id}" class="details-button">View Details</a>
    `;
    
    container.appendChild(card);
  });
}

function setupPriceFilter(places) {
  const priceFilter = document.getElementById('price-filter');
  if (!priceFilter) return;
  
  priceFilter.addEventListener('change', () => {
    const maxPrice = priceFilter.value;
    const placeCards = document.querySelectorAll('.place-card');
    
    placeCards.forEach(card => {
      const priceText = card.querySelector('.price').textContent;
      const price = parseFloat(priceText.replace('Price: $', ''));
      
      if (maxPrice === 'All' || price <= parseFloat(maxPrice)) {
        card.style.display = 'block';
      } else {
        card.style.display = 'none';
      }
    });
  });
}

async function fetchPlaceDetails(placeId) {
  if (!placeId) return;
  
  try {
    const token = getCookie('token');
    const headers = {
      'Content-Type': 'application/json'
    };
    
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    
    const res = await fetch(`/api/v1/places/${placeId}`, {
      headers: headers
    });
    
    if (!res.ok) throw new Error('Failed to load place details');
    const place = await res.json();
    displayPlaceDetails(place);
    
    fetchReviews(placeId);
  } catch (err) {
    console.error(err);
    const placeDetails = document.getElementById('place-details');
    if (placeDetails) {
      placeDetails.innerHTML = '<p class="error">Error loading place details</p>';
    }
  }
}

function displayPlaceDetails(place) {
  const container = document.getElementById('place-details');
  if (!container) return;
  
  const title = place.title || place.name || 'Unnamed Place';
  
  container.innerHTML = `
    <h1>${title}</h1>
    <div class="place-info">
      <p class="price">Price: $${place.price}</p>
      <p>${place.description || 'No description available'}</p>
      <div class="amenities">
        <h3>Amenities</h3>
        <div id="amenities-list"></div>
      </div>
    </div>
  `;
  
  const amenitiesList = document.getElementById('amenities-list');
  if (amenitiesList && place.amenities && place.amenities.length > 0) {
    place.amenities.forEach(amenity => {
      const tag = document.createElement('span');
      tag.className = 'amenity-tag';
      tag.textContent = amenity.name;
      amenitiesList.appendChild(tag);
    });
  } else if (amenitiesList) {
    amenitiesList.innerHTML = '<p>No amenities listed</p>';
  }
}

async function fetchReviews(placeId) {
  if (!placeId) return;
  
  try {
    const token = getCookie('token');
    const headers = {
      'Content-Type': 'application/json'
    };
    
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    
    const res = await fetch(`/api/v1/places/${placeId}/reviews`, {
      headers: headers
    });
    
    if (!res.ok) throw new Error('Failed to load reviews');
    const reviews = await res.json();
    displayReviews(reviews);
  } catch (err) {
    console.error(err);
    const reviewsList = document.getElementById('reviews-list');
    if (reviewsList) {
      reviewsList.innerHTML = '<p class="error">Error loading reviews</p>';
    }
  }
}

function displayReviews(reviews) {
  const container = document.getElementById('reviews-list');
  if (!container) return;
  
  container.innerHTML = '';

  if (reviews.length === 0) {
    container.innerHTML = '<p>No reviews yet. Be the first to review!</p>';
    return;
  }

  reviews.forEach(review => {
    const card = document.createElement('div');
    card.className = 'review-card';
    
    let stars = '';
    for (let i = 0; i < 5; i++) {
      if (i < review.rating) {
        stars += '★';
      } else {
        stars += '☆';
      }
    }
    
    const userName = review.user ? (review.user.first_name || 'Anonymous') : 'Anonymous';
    
    card.innerHTML = `
      <div class="review-header">
        <span class="reviewer-name">${userName}</span>
        <span class="review-rating">${stars}</span>
      </div>
      <p class="review-text">${review.text || review.comment || ''}</p>
      <small class="review-date">${new Date(review.created_at).toLocaleDateString()}</small>
    `;
    
    container.appendChild(card);
  });
}

async function submitReview(event) {
  event.preventDefault();
  
  const token = getCookie('token');
  if (!token) {
    alert('You must be logged in to submit a review');
    window.location.href = '/login';
    return;
  }
  
  const placeId = getPlaceIdFromURL();
  if (!placeId) {
    alert('Invalid place ID');
    return;
  }
  
  const comment = document.getElementById('comment').value.trim();
  const rating = parseInt(document.getElementById('rating').value, 10);
  
  if (!comment) {
    alert('Please enter your review');
    return;
  }
  
  if (isNaN(rating) || rating < 1 || rating > 5) {
    alert('Please enter a rating between 1 and 5');
    return;
  }
  
  try {
    const res = await fetch(`/api/v1/places/${placeId}/reviews`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ text: comment, rating: rating })
    });
    
    if (res.ok) {
      alert('Review submitted successfully!');
      document.getElementById('comment').value = '';
      document.getElementById('rating').value = '';
      
      fetchReviews(placeId);
    } else {
      const error = await res.json().catch(() => ({}));
      alert(error.msg || 'Failed to submit review');
    }
  } catch (err) {
    console.error(err);
    alert('Network error when submitting review');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const token = checkAuthentication();
  
  const logoutButton = document.getElementById('logout-button');
  if (logoutButton) {
    logoutButton.addEventListener('click', handleLogout);
  }

  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', handleLogin);
  }

  const placesList = document.getElementById('places-list');
  if (placesList) {
    fetchPlaces();
  }

  const placeDetails = document.getElementById('place-details');
  if (placeDetails) {
    const placeId = getPlaceIdFromURL();
    if (placeId) {
      fetchPlaceDetails(placeId);
      
      const addReviewSection = document.getElementById('add-review');
      if (addReviewSection) {
        if (token) {
          addReviewSection.style.display = 'block';
          
          const reviewForm = document.getElementById('review-form');
          if (reviewForm) {
            reviewForm.addEventListener('submit', submitReview);
          }
        } else {
          addReviewSection.style.display = 'none';
        }
      }
    } else {
      placeDetails.innerHTML = '<p class="error">No place ID specified</p>';
    }
  }
});