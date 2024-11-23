from django.urls import path 
from . import views

# Definimos las rutas de URLs específicas para la aplicación 'Chill and Sweet'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('create/', views.create, name = 'create'),
    path('customdesert/<int:categoria_id>/', views.customDessert, name = 'personalize'),
    path('help/', views.help_view, name='help'),
    path('orden/', views.orden, name='orden'),
    path('pago/', views.pago, name='pago'),
    path('contact/', views.contact, name='contact'),
    path('account/', views.account, name='account'),
    path('menu/', views.menu, name='menu'),
    path('favoritos/', views.favoritos, name='favoritos'),
    path('soon/', views.soon, name='soon'),
]