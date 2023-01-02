function alertGenerate(parentElement, text) {
    let alert = document.createElement('div')
        alert.className = 'alert alert-warning alert-dismissible fade show'
        alert.role = 'alert'
        alert.innerHTML = `
            ${text}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `
        
        parentElement.insertAdjacentElement('afterbegin', alert)
}

let loginBt = document.querySelector('#login-bt')
loginBt.addEventListener('click', (event) => {
    event.preventDefault()
    let loginBox = document.querySelector('.login-box')
    let userInput = document.querySelector('#email')
    let pwdInput = document.querySelector('#senha')
    let form = document.querySelector('#form')
    if (!userInput.value) {
        alertGenerate(loginBox, 'Usuário inválido')
    } else if (!pwdInput.value) {
        alertGenerate(loginBox, 'Senha inválida')
    } else {
        loginBt.innerHTML = '<div class="spinner-border spinner-border-sm text-info" role="status"></div>'
        form.submit()
    }
})