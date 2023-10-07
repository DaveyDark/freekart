const customerForm = document.getElementById('customerRegister')
const sellerForm = document.getElementById('sellerRegister')

customerForm.addEventListener('submit', e => {
  e.preventDefault()
  console.log(new FormData(customerForm))
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
