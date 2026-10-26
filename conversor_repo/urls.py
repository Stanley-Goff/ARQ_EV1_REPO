#Rutas de la aplicación

from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("historial/", views.ver_historial, name="historial"),
]