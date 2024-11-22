//Función para el funcionanmiento de los precio
document.addEventListener('DOMContentLoaded', () => {
    // Handle increment and decrement buttons
    const rows = document.querySelectorAll('.product-row');
    rows.forEach(row => {
        const incrementBtn = row.querySelector('.increment');
        const decrementBtn = row.querySelector('.decrement');
        const quantityElem = row.querySelector('.quantity');
        const unitPriceElem = row.querySelector('.unit-price');
        const subtotalElem = row.querySelector('.subtotal');
        const deleteBtn = row.querySelector('.delete-product');

        let quantity = parseInt(quantityElem.textContent, 10);
        const unitPrice = parseFloat(unitPriceElem.dataset.price);

        function updateSubtotal() {
            const subtotal = quantity * unitPrice;
            subtotalElem.textContent = `$${subtotal.toFixed(2)}`;
        }

        incrementBtn.addEventListener('click', () => {
            quantity += 1;
            quantityElem.textContent = quantity;
            updateSubtotal();
        });

        decrementBtn.addEventListener('click', () => {
            if (quantity > 1) {
                quantity -= 1;
                quantityElem.textContent = quantity;
                updateSubtotal();
            }
        });

        deleteBtn.addEventListener('click', () => {
            row.remove();
        });
    });
});

document.addEventListener('DOMContentLoaded', () => {
    function updateTotals() {
        const subtotals = document.querySelectorAll('.subtotal');
        const initialElem = document.querySelector('.initial');
        const totalElem = document.querySelector('.total');
        const pointsElem = document.querySelector('.points'); // Elemento que muestra el valor fijo de puntos
        let totalSum = 0;

        // Calcular la suma de todos los subtotales
        subtotals.forEach(subtotalElem => {
            const subtotalValue = parseFloat(subtotalElem.textContent.replace('$', '').trim());
            if (!isNaN(subtotalValue)) {
                totalSum += subtotalValue;
            }
        });

        // Mostrar el valor inicial
        initialElem.textContent = `Inicial: $${totalSum.toFixed(2)}`;

        // Obtener el valor de puntos (fijo) y calcular el total
        const pointsValue = parseFloat(pointsElem.textContent) || 0;
        let finalTotal = totalSum - pointsValue;
        if (finalTotal < 0) {
            finalTotal = 0; // Asegurar que el total no sea negativo
        }
        totalElem.textContent = `Total: $${finalTotal.toFixed(2)}`;
    }

    function handleProductRemoval(event) {
        let button = event.target;
        // Si se hace clic en la imagen, subir al botón padre
        if (button.tagName === 'IMG') {
            button = button.closest('.delete-product');
        }
    
        if (button && button.classList.contains('delete-product')) {
            const productRow = button.closest('.product-row');
            if (productRow) {
                productRow.remove();
                updateTotals();  // recalcular los totales al eliminar un producto
            }
        }
    }

    // llama a la función para calcular la suma inicial al cargar la página
    updateTotals();

    // manejar eventos de cambio para los botones de incremento/decremento
    const incrementBtns = document.querySelectorAll('.increment');
    const decrementBtns = document.querySelectorAll('.decrement');

    incrementBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            updateTotals();
        });
    });

    decrementBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            updateTotals();
        });
    });

    // Manejar el evento de eliminación de producto
    const table = document.querySelector('table');
    table.addEventListener('click', handleProductRemoval);
});

