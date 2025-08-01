function getCookie(name) {
  return document.cookie
    .split(';')
    .map(c => c.trim())
    .find(c => c.startsWith(name + '='))
    ?.split('=')[1] || null;
}

document.addEventListener('DOMContentLoaded', () => {
  const form   = document.getElementById('add-place-form');
  const msgDiv = document.getElementById('form-message');
  const token  = getCookie('token');

  if (!token) {
    window.location.replace('/login');
    return;
  }

  form.addEventListener('submit', async e => {
    e.preventDefault();
    msgDiv.textContent = '';
    msgDiv.className   = 'message';

    const body = {
      title:       document.getElementById('title').value.trim(),
      description: document.getElementById('description').value.trim(),
      price:       parseFloat(document.getElementById('price').value),
      latitude:    parseFloat(document.getElementById('latitude').value),
      longitude:   parseFloat(document.getElementById('longitude').value),
      amenities:   document.getElementById('amenities')
                    .value
                    .split(',')
                    .map(a => a.trim())
                    .filter(a => a.length > 0)
    };

    try {
      const resp = await fetch('/api/v1/places', {
        method: 'POST',
        headers: {
          'Content-Type':  'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(body)
      });
      const data = await resp.json();

      if (resp.ok) {
        msgDiv.textContent = `Place created! ID: ${data.id}`;
        msgDiv.classList.add('success');
        setTimeout(() => window.location.replace('/'), 2000);
      } else {
        msgDiv.textContent = data.message || data.msg || 'Error creating place';
        msgDiv.classList.add('error');
      }
    } catch (err) {
      console.error(err);
      msgDiv.textContent = 'Could not connect to server.';
      msgDiv.classList.add('error');
    }
  });
});
