const checkAuth = () => {
    const cookies = document.cookie.split(';');
    const token = cookies.find(cookie => cookie.trim().startsWith('token='));
    return token !== null;
};

if (!checkAuth() && window.location.pathname !== '/login') {
    window.location.href = '/login';
}

document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();

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
                    errorDiv.textContent = errorData.msg || 'Login failed.';
                    errorDiv.style.display = 'block';
                }
            } catch (error) {
                errorDiv.textContent = 'Could not connect to the server.';
                errorDiv.style.display = 'block';
            }
        });
    }
});

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token) {
        if (loginLink) loginLink.style.display = 'block';
    } else {
        if (loginLink) loginLink.style.display = 'none';
        fetchPlaces(token);
    }
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 1) return parts.pop().split(';').shift();
    return null;
}

async function fetchPlaces(token) {
    try {
        const response = await fetch('/api/v1/places', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        } else {
            console.error('Failed to fetch places:', response.statusText);
        }
    } catch (error) {
        console.error('Error fetching places:', error);
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;
    
    placesList.innerHTML = '';
    
    places.forEach(place => {
        const placeElement = document.createElement('div');
        placeElement.className = 'place-card';
        placeElement.dataset.price = place.price;
        placeElement.innerHTML = `
            <h3>${place.name || 'Unnamed Property'}</h3>
            <p>⭐ ${place.rating || 'N/A'} stars</p>
            <p>${place.description || 'No description'}</p>
            <p style="color: #aaa; margin-top: 15px;">Price per night: $${place.price}</p>
            <button class="details-button">View Details</button>
        `;
        placesList.appendChild(placeElement);
    });
}

document.getElementById('price-filter').addEventListener('change', (event) => {
    const selectedValue = event.target.value;
    const maxPrice = selectedValue === 'All' ? Infinity : parseFloat(selectedValue);
    const places = document.querySelectorAll('.place-card');

    places.forEach(place => {
        const price = parseFloat(place.dataset.price);
        place.style.display = price <= maxPrice ? 'block' : 'none';
    });
});