from django.contrib import admin
from django.urls import path, include

# Definimos las rutas de URLs principales del proyecto
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('orden/', include(('orden.urls', 'orden'), namespace='orden')),
    path('pago/', include(('pago.urls', 'pago'), namespace='pago'))
]
