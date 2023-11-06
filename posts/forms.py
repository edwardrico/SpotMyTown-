# Importations requises
from django import forms
from .models import Posts, Comment


# Formulaire pour la création de publication


class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'subtitle', 'description', 'imagen_posts', 'categorie']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': "Nom de l'établissement"}),
            'subtitle': forms.TextInput(attrs={'placeholder': 'Titre'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description'}),
            'categorie': forms.Select(choices=Posts.CATEGORIE_CHOICES, attrs={'class': 'form-control'}),
        }
        labels = {
            'categorie': 'Catégorie',
        }


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
