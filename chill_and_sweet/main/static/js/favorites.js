document.addEventListener('DOMContentLoaded', () => {
    // Seleccionar todos los botones de favoritos
    const favoriteButtons = document.querySelectorAll('.favorito-btn');

    favoriteButtons.forEach(button => {
        button.addEventListener('click', async (event) => {
            const postId = button.getAttribute('data-id');

            // Enviar solicitud AJAX al servidor
            try {
                const response = await fetch('/toggle_favorito/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'), // Obtener CSRF token
                    },
                    body: JSON.stringify({ postre_id: postId }),
                });

                const data = await response.json();

                if (data.success) {
                    // Actualizar visualmente el botón según el estado
                    if (data.favorited) {
                        button.classList.add('favorited'); // Agregar clase "favorited"
                    } else {
                        button.classList.remove('favorited'); // Quitar clase "favorited"
                    }
                } else {
                    console.error(data.message);
                }
            } catch (error) {
                console.error('Error al realizar la solicitud:', error);
            }
        });
    });

    // Función para obtener el token CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === name + '=') {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
