/**
 * Alterna la visibilidad del menú móvil y su overlay.
 * Abre o cierra el menú lateral (mobileMenu) y el overlay (mobileOverlay). 
 * Agrega o elimina clases para activar transiciones de apertura o cierre.
 */
function toggleMenu() {
    const overlay = document.getElementById('mobileOverlay');
    const menu = document.getElementById('mobileMenu');
    
    if (overlay.style.display === 'flex') {
        // Cierra el menú y oculta el overlay
        overlay.style.display = 'none';
        overlay.classList.remove('show-overlay');
        menu.classList.remove('show');
    } else {
        // Abre el menú y muestra el overlay con transición
        overlay.style.display = 'flex';
        setTimeout(() => {
            overlay.classList.add('show-overlay');
            menu.classList.add('show');
        }, 10);
    }
}
