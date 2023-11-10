from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),  # URL pour la page d'accueil
    path('about/', views.about, name="about"),  # URL pour la page à propos
]
