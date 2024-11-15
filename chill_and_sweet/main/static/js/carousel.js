// Inicializa el índice del slide en 1 (primer slide)
let slideIndex = 1;
showSlides(slideIndex);

/**
 * Muestra un slide específico basado en el índice proporcionado.
 * @param {number} n - Índice del slide a mostrar.
 */
function showSlides(n) {
    let slides = document.getElementsByClassName("slide");
    let dots = document.getElementsByClassName("dot");

    if (n > slides.length) { slideIndex = 1; }
    if (n < 1) { slideIndex = slides.length; }

    for (let i = 0; i < slides.length; i++) {
        slides[i].classList.remove("active");
    }
    for (let i = 0; i < dots.length; i++) {
        dots[i].classList.remove("active");
    }

    slides[slideIndex - 1].classList.add("active");
    dots[slideIndex - 1].classList.add("active");
}

/**
 * Cambia al siguiente o anterior slide.
 * @param {number} n - Valor a sumar al índice actual del slide.
 */
function nextSlide(n) {
    showSlides(slideIndex += n);
}

/**
 * Muestra un slide específico basado en su índice.
 * @param {number} n - Índice del slide a mostrar.
 */
function currentSlide(n) {
    showSlides(slideIndex = n);
}

// Cambia automáticamente al siguiente slide cada 5 segundos
setInterval(() => {
    nextSlide(1);
}, 5000);

// Variables para controlar el deslizamiento táctil
let startX;

// Selecciona el contenedor del carrusel para eventos de deslizamiento táctil
const carousel = document.querySelector('.carousel-image');

/**
 * Captura la posición inicial del deslizamiento.
 * @param {TouchEvent} e - Evento de inicio del toque.
 */
carousel.addEventListener('touchstart', (e) => {
    startX = e.touches[0].clientX;
});

/**
 * Maneja el final del deslizamiento y determina la dirección.
 * @param {TouchEvent} e - Evento de finalización del toque.
 */
carousel.addEventListener('touchend', (e) => {
    const endX = e.changedTouches[0].clientX;
    handleSwipe(endX);
});

/**
 * Determina si el deslizamiento cumple el umbral necesario para cambiar de slide.
 * @param {number} endX - Posición final del toque en el eje X.
 */
function handleSwipe(endX) {
    const swipeDistance = startX - endX; 
    const threshold = 50; 

    if (swipeDistance > threshold) {
        nextSlide(1);
    } else if (swipeDistance < -threshold) {
        nextSlide(-1);
    }
}
