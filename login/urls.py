from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('error_login/', views.error_login, name='error_login'),
    path('accounts/login/', views.custom_login, name='login'),  # URL pour la page de connexion
    path('logout/', views.custom_logout, name='logout'),  # URL pour la déconnexion
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    # URL pour la réinitialisation du mot de passe
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # URL pour la confirmation de la réinitialisation du mot de passe
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # URL pour confirmer la réinitialisation du mot de passe
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # URL pour la réinitialisation du mot de passe terminée

]
