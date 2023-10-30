#from django.shortcuts import render
#from .models import Posts
#from django.db.models import Q


#def search_posts(request):
    #query = request.GET.get('q')
    #category = request.GET.get('category')

    #if query and category:
        #results = Posts.objects.filter(
            #Q(title__icontains=query) & Q(categorie=category))

    #elif query:
        #results = Posts.objects.filter(
            #Q(title__icontains=query))

    #elif category:
        #results = Posts.objects.filter(
            #Q(categorie=category))

    #else:
        #results = Posts.objects.all()

    #return render(request, 'search/search_results.html', {'results': results, 'query': query, 'category': category})
