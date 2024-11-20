from django.contrib import admin
from django.urls import path, include

# Definimos las rutas de URLs principales del proyecto
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),   
    path('inicio/', include('inicio.urls')),
    path('menu/', include('menu.urls') ),
]
