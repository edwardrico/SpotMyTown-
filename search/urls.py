from django.urls import path
from . import views

urlpatterns = [

    path('search/', views.search_posts, name='search_posts'),
]
