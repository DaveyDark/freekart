const loginForm = document.getElementById('loginForm')

loginForm.addEventListener('submit', e => {
  e.preventDefault()
  fetch('/api/login', {
    method: "POST",
    body: new FormData(loginForm),
  }).then(res => {
    if(res.status == 200) {
      window.location = '/'
    } else {
      console.log(`Error: Server returned ${res.status}`)
    }
  }).catch(err => {
    console.log(`Error: ${err}`)
  })
})
