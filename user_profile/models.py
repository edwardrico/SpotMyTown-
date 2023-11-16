from django.db import models
from django.contrib.auth.models import User
from subscription.models import Subscription

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    prenom = models.CharField(max_length=30, blank=True, null=True)
    nom = models.CharField(max_length=30, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_picture', blank=True, null=True, default="user_icon.jpeg")
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=False, null=True)
    subscription = models.OneToOneField(Subscription, on_delete=models.CASCADE, null=True, blank=True, related_name='user_profile_subscription')

    def __str__(self):
        return f"UserProfile de {self.user}"
