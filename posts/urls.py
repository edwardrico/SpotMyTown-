from django.urls import path
from . import views

urlpatterns = [

    path('post/<uuid:pk>/', views.post, name='post'),
    path('post/<uuid:pk>/rate/', views.post_rating, name='post_rating'),
    path('commentaire/<uuid:pk>/', views.commentaire, name='commentaire'),  # URL pour les commentaires
    path('form_post/', views.formulaire, name='formPost'),  # URL pour afficher le formulaire de création de publication
    path('delete-post/<str:pk>/', views.deletePost, name='delete-post'),  # URL pour supprimer une publication
    path('update-post/<str:pk>/', views.updatePost, name='update-post'),  # URL pour mettre à jour une publication
    path('restaurant/', views.restaurant, name='restaurant'),  # URL pour afficher des publications dans la catégorie restaurant
    path('bar/', views.bar, name='bar'),  # URL pour afficher des publications dans la catégorie bar
    path('tourisme/', views.tourisme, name='tourisme'),  # URL pour afficher des publications dans la catégorie tourisme
    path('nightClubs/', views.nightClubs, name='nightClubs'),  # URL pour afficher des publications dans la catégorie nightClubs
    path('search_posts/', views.search_posts, name='search_posts'),  # URL pour la recherche de publications
    ]
