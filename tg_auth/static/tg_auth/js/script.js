function showPassword() {
    const btnPassword = document.querySelector('.form-password-btn');
    const inputPassword = document.querySelector('#password');

    btnPassword.addEventListener('click', () => {
        btnPassword.classList.toggle('active');

        if (inputPassword.getAttribute('type') === 'password') {
            inputPassword.setAttribute('type', 'text');
        } else {
            inputPassword.setAttribute('type', 'password');
        }
    })
}
showPassword()