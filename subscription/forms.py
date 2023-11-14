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

    def clean_prenom(self):
        prenom = self.cleaned_data['prenom']
        if not prenom.isalpha():
            raise forms.ValidationError("Le prénom ne doit contenir que des lettres.")
        return prenom

    def clean_nom(self):
        nom = self.cleaned_data['nom']
        if not nom.isalpha():
            raise forms.ValidationError("Le nom ne doit contenir que des lettres.")
        return nom
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Un utilisateur avec ce nom d'utilisateur existe déjà.")
        return username

    #def clean_email(self):
        #email = self.cleaned_data['email']
        #if User.objects.filter(email=email).exists():
            #raise forms.ValidationError("Un utilisateur avec cette adresse e-mail existe déjà.")
        #return email
