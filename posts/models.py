import uuid
from django.db import models
from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse
from user_profile.models import UserProfile
from django.utils import timezone



# Modèle pour stocker les publications

class Posts(models.Model):
    title = models.CharField(max_length=30, blank=False)  # Titre de la publication
    subtitle = models.CharField(max_length=100, blank=False, null=True)  # Sous-titre de la publication (optionnel)
    description = models.TextField(max_length=700, blank=False,
                                   null=True)  # Description de la publication (optionnelle)
    imagen_posts = models.ImageField(blank=False, null=False,
                                     default="default_image.png")  # Image associée à la publication
    image_width = models.PositiveIntegerField(default=350)  # Largeur souhaitée de l'image
    image_height = models.PositiveIntegerField(default=320)  # Hauteur souhaitée de l'image
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)  # ID unique
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création de la publication
    city = models.CharField(max_length=200, blank=True, null=True)


    # Ajoutez ces champs
    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)
    meta_description = models.CharField(max_length=255, blank=True, null=True)
    keywords = models.CharField(max_length=255, blank=True, null=True)

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
                                     blank=True)
    ratings = models.ManyToManyField(User, through='Rating',
                                     related_name='post_rating')  # Relation plusieurs à plusieurs avec les évaluations associées
    objects = models.Manager()

    def save(self, *args, **kwargs):
        if not self.title:
            # Si le champ title est vide, remplir avec un titre automatique en fonction du contenu.
            self.title = "Titre automatique en fonction du contenu de la publication"

        if not self.description:
            # Si le champ description est vide, remplir avec une description automatique en fonction du contenu.
            self.description = "Description automatique en fonction du contenu de la publication"

        if not self.keywords:
            # Si le champ keywords est vide, remplir avec des mots-clés automatiques en fonction du contenu.
            self.keywords = "Mots-clés automatiques en fonction du contenu de la publication"

        if not self.slug:
            # Si le champ slug est vide, générer un slug à partir du titre.
            self.slug = slugify(self.title)

        if not self.meta_description:
            # Si le champ meta_description est vide, remplir avec la description de la publication.
            self.meta_description = self.description

        if self.imagen_posts:
            try:
                image = Image.open(self.imagen_posts.path)
                image = image.resize((self.image_width, self.image_height), Image.ANTIALIAS)
                image.save(self.imagen_posts.path, 'JPEG', quality=90, optimize=True)
            except Exception as e:
                print(f"Error resizing image: {str(e)}")

        if not self.slug:
            self.slug = slugify(self.title)

        super(Posts, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


# Modèle pour stocker les commentaires
class Comment(models.Model):
    objects = None
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE, default=1)  # Relation plusieurs à un avec le modèle User (auteur du commentaire)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, default=1)  # Relation plusieurs à un avec la publication associée
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
