from django.urls import path
from . import views

# Definimos las rutas de URLs específicas para la aplicación 'Chill and Sweet'
urlpatterns = [
    path('', views.index_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
]
