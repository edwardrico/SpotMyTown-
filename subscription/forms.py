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
