document.addEventListener("DOMContentLoaded", function() {
    const togglePassword = document.querySelector('#togglePassword');
    const passwordField = document.querySelector('#id_password');

    togglePassword.addEventListener('click', function() {
        // Toggle the type attribute
        const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordField.setAttribute('type', type);

        // Toggle the icon
        this.firstElementChild.classList.toggle('bi-eye');
        this.firstElementChild.classList.toggle('bi-eye-slash');
    });
});
