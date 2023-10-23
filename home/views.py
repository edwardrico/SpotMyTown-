from django.shortcuts import render
from posts.models import Posts


# Create your views here.

def home(request):
    # Récupérer toutes les publications triées par date de création décroissante
    posts = Posts.objects.all().order_by('-created_at')
    context = {'posts': posts}
    return render(request, 'home/home.html', context)
