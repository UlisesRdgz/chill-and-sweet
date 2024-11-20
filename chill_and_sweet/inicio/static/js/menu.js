function toggleMenu() {
    const overlay = document.getElementById('mobileOverlay');
    const menu = document.getElementById('mobileMenu');
    
    if (overlay.style.display === 'flex') {
        overlay.style.display = 'none';
        overlay.classList.remove('show-overlay');
        menu.classList.remove('show');
    } else {
        overlay.style.display = 'flex';
        setTimeout(() => {
            overlay.classList.add('show-overlay');
            menu.classList.add('show');
        }, 10);
    }
}        