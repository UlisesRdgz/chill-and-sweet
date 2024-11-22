document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('#paymentForm');
    const payButton = document.querySelector('#payButton');

    form.addEventListener('submit', (event) => {
        event.preventDefault(); // Evita el envío del formulario
        let isValid = true;

        // Validar el nombre del titular
        const nombre = document.querySelector('input[placeholder="Nombre"]').value.trim();
        if (!nombre || nombre.length < 3) {
            alert('El nombre del titular debe tener al menos 3 caracteres.');
            isValid = false;
        }

        // Validar el número de la tarjeta (16 dígitos)
        const cardNumber = document.querySelector('#cardNumber');
        if (cardNumber.value.length !== 16 || !/^\d{16}$/.test(cardNumber.value)) {
            cardNumber.nextElementSibling.classList.remove('hidden');
            isValid = false;
        } else {
            cardNumber.nextElementSibling.classList.add('hidden');
        }

        // Validar la fecha de expiración (MM/YY)
        const expiracion = document.querySelector('input[placeholder="MM/YY"]').value;
        if (!/^(0[1-9]|1[0-2])\/\d{2}$/.test(expiracion)) {
            alert('La fecha de expiración debe tener el formato MM/YY.');
            isValid = false;
        }

        // Validar el CVV (3 dígitos)
        const cvv = document.querySelector('input[placeholder="123"]').value;
        if (!/^\d{3}$/.test(cvv)) {
            alert('El CVV debe tener 3 dígitos.');
            isValid = false;
        }

        // Validar la ciudad
        const ciudad = document.querySelector('input[placeholder="Ciudad"]').value.trim();
        if (!ciudad) {
            alert('Por favor ingresa una ciudad.');
            isValid = false;
        }

        // Validar el código postal (CP) - 5 dígitos
        const cp = document.querySelector('input[placeholder="12345"]').value;
        if (!/^\d{5}$/.test(cp)) {
            alert('El código postal debe tener 5 dígitos.');
            isValid = false;
        }

        // Si todas las validaciones pasan, habilitar el botón de Pagar
        if (isValid) {
            alert('Datos válidos. Puedes proceder a pagar.');
            payButton.disabled = false;
        }
    });
});


//Para el funcionamiento del modal
function showModal() {
    document.getElementById('thankYouModal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('thankYouModal').style.display = 'none';
}

function selectPaymentMethod(button) {
    const buttons = document.querySelectorAll('#paymentOptions button');
    buttons.forEach(btn => btn.classList.remove('selected'));
    button.classList.add('selected');
}

