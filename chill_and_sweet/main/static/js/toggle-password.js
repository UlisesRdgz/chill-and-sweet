document.addEventListener("DOMContentLoaded", function () {
    const togglePasswordIcons = document.querySelectorAll(".toggle-password");

    togglePasswordIcons.forEach(icon => {
        icon.addEventListener("click", function () {
            const passwordInput = this.previousElementSibling;
            const iconElement = this.querySelector("i");

            // Alterna el tipo de input entre "password" y "text"
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
