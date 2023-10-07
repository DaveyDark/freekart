const customerForm = document.getElementById('customerRegister')
const sellerForm = document.getElementById('sellerRegister')

const locationButton = document.getElementById('locationButton');
const latFields = document.getElementsByClassName('lat');
const longFields = document.getElementsByClassName('long');

locationButton.addEventListener('click', e => {
  if ('geolocation' in navigator) {
    navigator.geolocation.getCurrentPosition(position => {
      const latitude = position.coords.latitude;
      const longitude = position.coords.longitude;

      for (const latField of latFields) {
        latField.value = latitude;
      }

      for (const longField of longFields) {
        longField.value = longitude;
      }
    }, error => {
      console.error('Error getting location:', error);
    });
  } else {
    console.error('Geolocation is not available in this browser.');
  }
});

customerForm.addEventListener('submit', e => {
  e.preventDefault()
  fetch('/api/register/customer', {
    method: 'POST',
    body: new FormData(customerForm),
  }).then(res => {
    if(res.status == 201) {
      window.location = '/'
    } else {
      console.log(`Error Registering: Server returned ${res.status}`)
    }
  }).catch(err => {
      console.log(`Error Registering: ${err}`)
  })
})

sellerForm.addEventListener('submit', e => {
  e.preventDefault()
  fetch('/api/register/seller', {
    method: 'POST',
    body: new FormData(sellerForm),
  }).then(res => {
    if(res.status == 201) {
      window.location = '/'
    } else {
      console.log(`Error Registering: Server returned ${res.status}`)
    }
  }).catch(err => {
      console.log(`Error Registering: ${err}`)
  })
})
