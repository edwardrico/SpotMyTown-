from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name="home"),  # URL pour la page d'accueil
    path('post/<str:pk>', views.post, name="post"),  # URL pour afficher une publication individuelle
    path('post/<uuid:pk>/rate/', views.post_rating, name='post_rating'),
    path('commentaire/<uuid:pk>/', views.commentaire, name='commentaire'),  # URL pour les commentaires
    path('form_post/', views.formulaire, name='formPost'),  # URL pour afficher le formulaire de création de publication
    path('delete-post/<str:pk>/', views.deletePost, name='delete-post'),  # URL pour supprimer une publication
    path('update-post/<str:pk>/', views.updatePost, name='update-post'),  # URL pour mettre à jour une publication
    path('restaurant/', views.restaurant, name='restaurant'),  # URL pour afficher des publications dans la catégorie restaurant
    path('bar/', views.bar, name='bar'),  # URL pour afficher des publications dans la catégorie bar
    path('tourisme/', views.tourisme, name='tourisme'),  # URL pour afficher des publications dans la catégorie tourisme
    path('nightClubs/', views.nightClubs, name='nightClubs'),  # URL pour afficher des publications dans la catégorie nightClubs
    path('login/', views.custom_login, name='login'),  # URL pour la page de connexion
    path('logout/', views.custom_logout, name='logout'),  # URL pour la déconnexion
    path('register/', views.register, name='register'),  # URL pour l'inscription d'un nouvel utilisateur
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),  # URL pour la réinitialisation du mot de passe
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),  # URL pour la confirmation de la réinitialisation du mot de passe
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),  # URL pour confirmer la réinitialisation du mot de passe
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),  # URL pour la réinitialisation du mot de passe terminée
    path('profile/', views.view_profile, name='view_profile'),  # URL pour afficher le profil de l'utilisateur
    path('edit_profile/', views.edit_profile, name='edit_profile'),  # URL pour modifier le profil de l'utilisateur
]
