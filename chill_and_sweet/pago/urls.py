from django.urls import path
from . import views

app_name='pago'

urlpatterns = [
     path('',views.pago),
     path('', views.mostrar_pago, name='mostrar_pago'),
]