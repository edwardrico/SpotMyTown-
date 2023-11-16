from django import forms
from user_profile.models import UserProfile


# Formulaire pour le profil d'utilisateur
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_pic', 'bio', 'location']
