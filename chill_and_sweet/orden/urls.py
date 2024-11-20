from django.urls import path
from . import views

urlpatterns = [
     path('',views.orden),
      path('guardar_orden/', views.guardar_orden, name='guardar_orden'),
]