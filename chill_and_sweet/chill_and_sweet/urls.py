from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Definimos las rutas de URLs principales del proyecto
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
]

# En modo DEBUG, permite servir archivos multimedia desde MEDIA_URL.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)