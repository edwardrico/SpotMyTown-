from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render, redirect


# Vue pour la connexion de l'utilisateur
def custom_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()

    if not request.user.is_authenticated:
        message = "Vous devez être connecté pour accéder à cette page."
    else:
        message = None

    return render(request, 'register/login.html', {'form': form})


# Vue pour la déconnexion de l'utilisateur
def custom_logout(request):
    logout(request)
    return redirect('home')


# Classe pour la vue personnalisée de réinitialisation du mot de passe
class CustomPasswordResetView(PasswordResetView):
    # Spécifie le modèle de la page de réinitialisation du mot de passe
    template_name = 'registration/password_reset_form.html'

    # Spécifie le modèle de l'e-mail envoyé pour réinitialiser le mot de passe
    email_template_name = 'registration/password_reset_email.html'

    # Spécifie le modèle de l'objet (sujet) de l'e-mail
    subject_template_name = 'registration/password_reset_subject.txt'

    # URL de redirection après une réinitialisation de mot de passe réussie
    success_url = '/password_reset/done/'
