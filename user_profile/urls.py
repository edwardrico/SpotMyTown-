from django.urls import path
from . import views

urlpatterns = [

    path('profile/', views.view_profile, name='view_profile'),  # URL pour afficher le profil de l'utilisateur
    path('edit_profile/', views.edit_profile, name='edit_profile'),  # URL pour modifier le profil de l'utilisateur
]


