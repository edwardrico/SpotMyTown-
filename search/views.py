from django.shortcuts import render
from .models import Posts
from django.db.models import Q


# Create your views here.

def search_posts(request):
    query = request.GET.get('q')
    category = request.GET.get('category')

    results = Posts.objects.filter(Q(title__icontains=query), categorie=category)

    return render(request, 'search/search_results.html', {'results': results, 'query': query, 'category': category})
