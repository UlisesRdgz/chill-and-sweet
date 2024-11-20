/**
 * Escucha el evento de carga completa del DOM y agrega funcionalidad de 
 * mostrar/ocultar contraseña a los íconos de alternancia.
 */
document.addEventListener("DOMContentLoaded", function () {
    const togglePasswordIcons = document.querySelectorAll(".toggle-password");

    togglePasswordIcons.forEach(icon => {
        icon.addEventListener("click", function () {
            const passwordInput = this.previousElementSibling;
            const iconElement = this.querySelector("i");

            if (passwordInput.type === "password") {
                passwordInput.type = "text"; 
                iconElement.classList.remove("fa-eye-slash");
                iconElement.classList.add("fa-eye");
            } else {
                passwordInput.type = "password"; 
                iconElement.classList.remove("fa-eye");
                iconElement.classList.add("fa-eye-slash");
            }
        });
    });
});
