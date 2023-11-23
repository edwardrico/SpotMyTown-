from django.contrib.auth import login, logout, authenticate
from .forms import CustomAuthenticationForm
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render, redirect
from django.contrib import messages
from user_profile.models import UserProfile
from .forms import CustomAuthenticationForm


def error_login(request):
    return render(request, '404/error_login.html')



# Vue pour la connexion de l'utilisateur
def custom_login(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(data=request.POST)  # Utilisez CustomAuthenticationForm ici
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                user_profile = UserProfile.objects.filter(user=user).first()

                if user_profile and user_profile.subscription.email_verified:
                    login(request, user)
                    return redirect('home')
                elif user_profile and not user_profile.subscription.email_verified:
                    messages.error(request, 'Veuillez vérifier votre email avant de vous connecter.')
                else:
                    messages.error(request, 'Profil non trouvé pour cet utilisateur.')
            else:
                messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')

            # Ajoutez ceci pour appeler la fonction JavaScript en cas d'erreur
            return render(request, 'login/login.html', {'form': form, 'error_popup': True})
        else:
            # Aucun besoin de réinitialiser form.error_messages['__all__'] ici
            messages.error(request, 'Erreur de connexion. Veuillez vérifier vos informations.')

            # Ajoutez ceci pour retourner le formulaire avec les erreurs
            return render(request, 'login/login.html', {'form': form, 'error_popup': True})
    else:
        form = CustomAuthenticationForm()  # Utilisez CustomAuthenticationForm ici

    if not request.user.is_authenticated:
        message = "Vous devez être connecté pour accéder à cette page."
    else:
        message = None

    return render(request, 'login/login.html', {'form': form, 'message': message})

def custom_logout(request):
    logout(request)
    return redirect('home')


# Classe pour la vue personnalisée de réinitialisation du mot de passe
class CustomPasswordResetView(PasswordResetView):
    # Spécifie le modèle de la page de réinitialisation du mot de passe
    template_name = 'login/password_reset_form.html'

    # Spécifie le modèle de l'e-mail envoyé pour réinitialiser le mot de passe
    email_template_name = 'login/password_reset_email.html'

    # Spécifie le modèle de l'objet (sujet) de l'e-mail
    subject_template_name = 'login/password_reset_subject.txt'

    # URL de redirection après une réinitialisation de mot de passe réussie
    success_url = '/password_reset/done/'
