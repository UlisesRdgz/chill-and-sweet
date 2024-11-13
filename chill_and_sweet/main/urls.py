from django.urls import path
from . import views

# Definimos las rutas de URLs específicas para la aplicación 'Chill and Sweet'
urlpatterns = [
    path('', views.index, name='index'),
    # path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
]
