// Función para cerrar manualmente la notificación
function cerrarNotificacion() {
    const alerta = document.getElementById('alerta-carrito');
    alerta.classList.add('oculto');
}

// Función para obtener parámetros de la URL
function getUrlParameter(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}

// Verifica si el parámetro "success" está presente
if (getUrlParameter('success') === 'true') {
    const alerta = document.getElementById('alerta-carrito');

    alerta.classList.remove('oculto');

    setTimeout(() => {
        alerta.classList.add('oculto');
    }, 3000);

    const newUrl = window.location.href.split('?')[0];
    window.history.replaceState({}, document.title, newUrl);
}

document.addEventListener('DOMContentLoaded', function () {
    const slider = document.getElementById('slider');
    const next = document.getElementById('next');
    const prev = document.getElementById('prev');
  
    next.addEventListener('click', () => {
      slider.scrollLeft += slider.offsetWidth;
    });
  
    prev.addEventListener('click', () => {
      slider.scrollLeft -= slider.offsetWidth;
    });
  });
