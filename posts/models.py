import uuid
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Modèle pour stocker les informations de profil utilisateur
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relation un à un avec le modèle User
    profile_pic = models.ImageField(upload_to='profile_picture', blank=True, null=True, default="user_icon.jpeg")
    bio = models.TextField(blank=True, null=True)  # Champ pour la biographie de l'utilisateur
    location = models.CharField(max_length=100, blank=False, null=True)  # Champ pour la localisation de l'utilisateur

    def __str__(self):
        return f"UserProfile de {self.user}"  # Représentation textuelle de l'objet (nom d'utilisateur)


# Modèle pour gérer les abonnements des utilisateurs
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relation plusieurs à un avec le modèle User
    active = models.BooleanField(default=False)  # Indique si l'abonnement est actif
    first_name = models.CharField(max_length=30, blank=False, null=True)  # Champ pour le prénom de l'utilisateur
    last_name = models.CharField(max_length=30, blank=False, null=True)  # Champ pour le nom de l'utilisateur

    def __str__(self):
        return f"Abonnement de {self.user} - {self.first_name} {self.last_name}"


# Modèle pour stocker les publications
class Posts(models.Model):
    title = models.CharField(max_length=30, blank=False)  # Titre de la publication
    subtitle = models.CharField(max_length=100, blank=False, null=True)  # Sous-titre de la publication (optionnel)
    description = models.TextField(max_length=700, blank=False, null=True)  # Description de la publication (optionnelle)
    imagen_posts = models.ImageField(blank=True, null=True,
                                     default="default_image.png")  # Image associée à la publication
    largeur_image = models.PositiveIntegerField(default=450)  # Largeur de l'image par défaut
    hauteur_image = models.PositiveIntegerField(default=350)  # Hauteur de l'image par défaut
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)  # ID unique
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création de la publication
    address = models.CharField(max_length=200, blank=True, null=True)

    # Choix de catégorie pour les publications
    CATEGORIE_CHOICES = [
        ('restaurant', 'Restaurant'),
        ('bar', 'Bar'),
        ('tourisme', 'Tourisme'),
        ('nightClubs', 'Night clubs'),
    ]
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES)  # Catégorie de la publication
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             default=1)  # Relation plusieurs à un avec le modèle User (utilisateur créateur de la publication)
    comments = models.ManyToManyField('Comment',
                                      related_name='post_comments')  # Relation plusieurs à plusieurs avec les commentaires associés
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_posts', null=True,
                                     blank=True)  # Relation plusieurs à un avec le profil utilisateur associé
    ratings = models.ManyToManyField(User, through='Rating',
                                     related_name='post_rating')  # Relation plusieurs à plusieurs avec les évaluations associées
    objects = models.Manager()

    def __str__(self):
        return self.title  # Représentation textuelle de l'objet (titre de la publication)


# Modèle pour stocker les commentaires
class Comment(models.Model):
    objects = None
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)  # Relation plusieurs à un avec le modèle User (auteur du commentaire)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)  # Relation plusieurs à un avec la publication associée
    text = models.TextField()  # Contenu du commentaire
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création du commentaire
    parent_comment = models.ForeignKey('self', null=True, blank=True,
                                       on_delete=models.CASCADE)  # Relation un à plusieurs pour les commentaires parentaux (réponses)

    def __str__(self):
        if self.user:
            return f"comment by {self.user.username if self.user else 'Anonyme'} on {self.post.title}"
        else:
            return "Anonyme"

    def get_absolute_url(self):
        return reverse('post', args=[str(self.post.id)])  # Lien vers la page de la publication associée


# models rating evaloution et compter de rating user sur les posts
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return f"rating by {self.user.username} on {self.post.title}"

    def get_absolute_url(self):
        return reverse('post', args=[str(self.post.id)])
