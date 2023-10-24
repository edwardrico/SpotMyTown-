from django.urls import path
from . import views

urlpatterns = [
    path('register_success/', views.register_success, name='register_success'),  # URL pour la confirmation de l'inscription
    path('register/', views.register, name='register'),  # URL pour l'inscription d'un nouvel utilisateur

]
