from django.db import models
from django.contrib.auth.models import User


# Modèle pour stocker les informations de profil utilisateur
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relation un à un avec le modèle User
    profile_pic = models.ImageField(upload_to='profile_picture', blank=True, null=True, default="user_icon.jpeg")
    bio = models.TextField(blank=True, null=True)  # Champ pour la biographie de l'utilisateur
    location = models.CharField(max_length=100, blank=False, null=True)  # Champ pour la localisation de l'utilisateur

    def __str__(self):
        return f"UserProfile de {self.user}"  # Représentation textuelle de l'objet (nom d'utilisateur)
