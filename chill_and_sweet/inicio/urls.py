from django.urls import path
from . import views

urlpatterns = [
    path('',views.inicio, name='inicio'),
    path('menu', views.menu, name='menu'),
]