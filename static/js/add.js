const form = document.getElementById('addForm')

form.addEventListener('submit', e => {
  e.preventDefault()
  console.log(new FormData(form))
  fetch('/api/products/add', {
    method: "POST",
    body: new FormData(form),
  }).then(res => {
    if(res.status == 201) {
      window.location = '/'
    } else {
      console.log(`Error: Server returned ${res.status}`)
    }
  }).catch(err => {
    console.log(`Error: ${err}`)
  })
})
