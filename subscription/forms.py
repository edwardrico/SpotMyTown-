from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


# Formulaire personnalisé d'inscription
class CustomRegistrationForm(UserCreationForm):
    prenom = forms.CharField(max_length=30, required=True, help_text='Optional.')
    nom = forms.CharField(max_length=30, required=True, help_text='Optional.')

    class Meta:
        model = User
        fields = ['prenom', 'nom', 'username', 'email', 'password1', 'password2']
        labels = {
            'prenom': 'Prénom',  # Étiquette personnalisée pour le champ "prenom"
            'nom': 'Nom',  # Étiquette personnalisée pour le champ "nom"
            'username': 'Nom d\'utilisateur',  # Étiquette personnalisée pour le champ "username"
            'email': 'Adresse e-mail',  # Étiquette personnalisée pour le champ "email"
            'password1': 'Mot de passe',  # Étiquette personnalisée pour le champ "password1"
            'password2': 'Confirmation du mot de passe',  # Étiquette personnalisée pour le champ "password2"
        }