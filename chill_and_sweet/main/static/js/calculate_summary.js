 // Función para actualizar el resumen, el precio total y las calorías totales
function actualizarResumen() {
    const opciones = document.querySelectorAll('.input_option');
    let total = 0;
    let caloriasTotales = 0;
    const ingredientesSeleccionados = [];

    opciones.forEach(input => {
        if (input.checked) {
            // Si la opción está seleccionada, agrega el nombre y el precio al resumen
            ingredientesSeleccionados.push(input.getAttribute('data-nombre'));
            total += parseFloat(input.getAttribute('data-precio'));
            caloriasTotales += parseInt(input.getAttribute('data-calorias')); // Suma las calorías
        }
    });

    // Actualiza el resumen de ingredientes en el DOM
    const listaIngredientes = document.getElementById('ingredientes-seleccionados');
    listaIngredientes.innerHTML = '';

    ingredientesSeleccionados.forEach(ingrediente => {
        const li = document.createElement('li');
        li.textContent = ingrediente;
        listaIngredientes.appendChild(li);
    });

    // Actualiza el total en el DOM
    const totalPrecio = document.getElementById('total-precio');
    totalPrecio.textContent = total.toFixed(2); // Muestra el total con dos decimales

    // Actualiza las calorías totales en el DOM
    const totalCalorias = document.querySelector('.total-calories');
    totalCalorias.textContent = `${caloriasTotales} cal`; // Muestra las calorías totales
}

// Asigna un evento a todos los inputs de tipo radio
const opciones = document.querySelectorAll('.input_option');
opciones.forEach(input => {
    input.addEventListener('change', actualizarResumen);
});
