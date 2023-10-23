from django.urls import path
from . import views

urlpatterns = [

    path('register/', views.register, name='register'),  # URL pour l'inscription d'un nouvel utilisateur

]
