from django import forms
from posts.models import Posts


class SearchForm(forms.Form):
    q = forms.CharField(label='Rechercher', required=False, widget=forms.TextInput(attrs={'placeholder': 'Rechercher...'}))
    category = forms.ChoiceField(label='Catégorie', required=False, choices=[('', 'Toutes les catégories')] + Posts.CATEGORIE_CHOICES)


