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
    path('custom_desert/<int:categoria_id>/', views.custom_dessert, name = 'personalize'),
    path('help/', views.help_view, name='help'),
    path('pago/', views.pago, name='pago'),
    path('contact/', views.contact, name='contact'),
    path('account/', views.account, name='account'),
    path('menu/', views.menu, name='menu'),
    path('favoritos/', views.favoritos, name='favoritos'),
    path('soon/', views.soon, name='soon'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('delete_from_cart/', views.delete_from_cart, name='delete_from_cart'),
    path('confirm_order/', views.confirm_order, name='confirm_order'),
    path('order/', views.order, name='order'),
    path('toggle_favorito/', views.toggle_favorito, name='toggle_favorito'),
]