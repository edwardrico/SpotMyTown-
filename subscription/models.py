from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# Modèle pour gérer les abonnements des utilisateurs
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relation plusieurs à un avec le modèle User
    active = models.BooleanField(default=False)  # Indique si l'abonnement est actif
    first_name = models.CharField(max_length=30, blank=False, null=True)  # Champ pour le prénom de l'utilisateur
    last_name = models.CharField(max_length=30, blank=False, null=True)  # Champ pour le nom de l'utilisateur

    def __str__(self):
        return f"Abonnement de {self.user} - {self.first_name} {self.last_name}"


