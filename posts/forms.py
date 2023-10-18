# Importations requises
from django.contrib.auth.models import User
from django import forms
from .models import Posts, UserProfile, Comment
from django.contrib.auth.forms import UserCreationForm


# Formulaire pour la création de publication
class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'subtitle', 'description', 'imagen_posts', 'categorie']
        labels = {
            'title': "Nom de l'établissement",  # Étiquette personnalisée pour le champ "title"
            'subtitle': 'Titre',  # Étiquette personnalisée pour le champ "subtitle"
            'description': 'Description',  # Étiquette personnalisée pour le champ "description"
            'imagen_posts': 'Image',  # Étiquette personnalisée pour le champ "imagen_posts"
            'categorie': 'Catégorie',  # Étiquette personnalisée pour le champ "categorie"
        }


# Formulaire personnalisé d'inscription
class CustomRegistrationForm(UserCreationForm):
    prenom = forms.CharField(max_length=30, required=True, help_text='Optional.')
    nom = forms.CharField(max_length=30, required=True, help_text='Optional.')

    class Meta:
        model = User
        fields = ['prenom', 'nom', 'username', 'email', 'password1', 'password2']


# Formulaire pour le profil d'utilisateur
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_pic', 'bio', 'location']


# Formulaire pour les commentaires
class CommentForm(forms.ModelForm):
    parent_comment = forms.ModelChoiceField(queryset=Comment.objects.all(), required=False)

    class Meta:
        model = Comment
        fields = ['text', 'parent_comment']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class PostRatingForm(forms.Form):
    RATING_CHOICES = [(0, '5'), (1, '1'), (1.5, '1.5'), (2, '2'), (2.5, '2.5'), (3, '3'), (3.5, '3.5'), (4, '4'),
                      (4.5, '4.5'), (5, '5')]
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect())
