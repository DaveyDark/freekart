const form = document.getElementById('addForm')

form.addEventListener('submit', e => {
  e.preventDefault()
  body = new FormData(form)
  const prod_id = parseInt(window.location.pathname.split('/').pop(), 10);
  body.append('id', prod_id)
  fetch('/api/products/edit', {
    method: "POST",
    body: body,
  }).then(res => {
    if(res.status == 200) {
      window.location = '/dashboard'
    } else {
      console.log(`Error: Server returned ${res.status}`)
    }
  }).catch(err => {
    console.log(`Error: ${err}`)
  })
})
