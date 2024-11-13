document.addEventListener("DOMContentLoaded", function() {
    const togglePassword = document.querySelector(".toggle-password");
    const passwordInput = document.querySelector("#password");

    togglePassword.addEventListener("click", function() {
        // Alterna el tipo de input entre "password" y "text"
        const type = passwordInput.getAttribute("type") === "password" ? "text" : "password";
        passwordInput.setAttribute("type", type);

        // Cambia entre el ícono de ojo abierto y cerrado de Font Awesome
        const icon = this.querySelector('i');
        icon.classList.toggle("fa-eye");
        icon.classList.toggle("fa-eye-slash");
    });
});