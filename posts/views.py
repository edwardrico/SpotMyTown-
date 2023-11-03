from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg, Q, Sum
from django.http import HttpResponseForbidden, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify
from .models import Posts, Comment, Rating
from .forms import PostForm, CommentForm, PostRatingForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Vue pour afficher une publication individuelle
def post(request, pk, ):
    try:
        post = Posts.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404("La publication n'existe pas")

    comments = Comment.objects.filter(post=post, parent_comment=None).order_by('-created_at')
    ratings = Rating.objects.filter(post=post)
    average_rating = ratings.aggregate(Avg('rating'))['rating__avg']
    rating_count = ratings.count()
    scale_min = 1
    scale_max = 5

    average_rating = max(scale_min, min(scale_max, average_rating or scale_min))
    average_star = int(average_rating)
    stars_css_class = "fa-star-checked" if average_star >= 0.5 else ""

    similar_posts = Posts.objects.filter(categorie=post.categorie).exclude(id=pk)[:4]

    category_counts = {
        'restaurant': Posts.objects.filter(categorie='restaurant').count(),
        'bar': Posts.objects.filter(categorie='bar').count(),
        'tourisme': Posts.objects.filter(categorie='tourisme').count(),
        'night_clubs': Posts.objects.filter(categorie='night clubs').count(),
    }

    comment_form = CommentForm()
    rating_form = PostRatingForm()

    if request.method == 'POST':
        if 'comment_submit' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.post = post
                comment.save()
                return redirect('post', pk=pk)

        if 'rating_submit' in request.POST:
            rating_form = PostRatingForm(request.POST)
            if rating_form.is_valid():
                rating = rating_form.cleaned_data['rating']
                user_rating, created = Rating.objects.get_or_create(user=request.user, post=post)
                user_rating.rating = rating
                user_rating.save()
                return redirect('post', pk=pk)

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'category_counts': category_counts,
        'similar_posts': similar_posts,
        'ratings': ratings,
        'rating_form': rating_form,
        'average_rating': average_rating,
        'stars_css_class': stars_css_class,
        'rating_count': rating_count,

    }
    return render(request, 'posts/posts.html', context)


@login_required
def post_rating(request, pk):
    post = get_object_or_404(Posts, id=pk)
    if request.method == 'POST':
        form = PostRatingForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            user_rating = Rating.objects.filter(user=request.user, post=post)
            if user_rating.exists():
                user_rating.update(rating=rating)
            else:
                Rating.objects.create(user=request.user, post=post, rating=rating)

            post.average_rating = Rating.objects.filter(post=post).aggregate(Avg('rating'))['rating__avg']
            post.save()
            return redirect('post', pk=pk)
    else:
        form = PostRatingForm()
    return redirect('post', pk=pk, )


def search_posts(request):
    query = request.GET.get('q')
    category = request.GET.get('category')

    title = ""
    results_count = 0

    if query and category:
        results = Posts.objects.filter(
            Q(title__iexact=query) & Q(categorie=category))
        title = f"Résultats pour {query} dans la catégorie {category}"

    elif query:
        results = Posts.objects.filter(
            Q(title__iexact=query))
        title = f"Resultats pour {query}"

    elif category:
        results = Posts.objects.filter(
            Q(categorie=category))
        title = f"Résultats dans {category}"

    else:
        results = Posts.objects.all()

    results_count = results.count()

    for post in results:
        post.average_rating = Rating.objects.filter(post=post).aggregate(Avg('rating'))['rating__avg'] or 0
        post.rating_count = Rating.objects.filter(post=post).count()

    total_ratings = results.aggregate(Sum('rating__rating'))['rating__rating__sum'] or 0

    ratings_count = Rating.objects.filter(post__in=results).count()

    percentage = 0

    context = {
        'results': results,
        'title': title,
        'query': query,
        'category': category,
        'results_count': results_count,
        'total_ratings': total_ratings,
        'ratings_count': ratings_count,
        'percentage': percentage,

    }

    print(f'context: {context}')
    return render(request, 'search/search_results.html', context)


# Vues pour les commentaries
@login_required
def commentaire(request, pk):
    post = Posts.objects.get(id=pk)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            parent_comment = comment_form.cleaned_data.get('parent_comment')  # Obtenez le commentaire parent
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = post
            if parent_comment:
                comment.parent_comment = parent_comment  # Liez la réponse au commentaire parent
            comment.save()
            return redirect('post', pk=pk)

    return redirect('post', pk=pk)


# Vue pour afficher un formulate de creation de publication
@login_required
def formulaire(request):
    if not request.user.is_authenticated:
        # Si l'utilisateur n'est pas connecté, redirigez-le vers la page de connexion
        return redirect('login')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.slug = generate_unique_slug(post.title, Posts)
            categorie = post.categorie
            post.save()
            # Rediriger l'utilisateur vers la page de la catégorie appropriée
            return redirect(reverse(categorie))

    else:
        form = PostForm()

    context = {'form': form}
    return render(request, 'posts/form_post.html', context)


def generate_unique_slug(title, model):
    slug = slugify(title)
    unique_slug = slug
    counter = 1
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{slug}-{counter}"
        counter += 1
    return unique_slug


# Vue pour supprimer une publication
@login_required
def deletePost(request, pk):
    post = Posts.objects.get(id=pk)

    # Vérifiez si l'utilisateur actuel est le créateur de la publication
    if post.user != request.user:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à supprimer ce post.")

    if request.method == 'POST':
        post.delete()
        category_url = reverse(post.categorie)
        return redirect(category_url)

    context = {'post': post}
    return render(request, 'posts/delete_post.html', context)


# Vue pour mettre à jour une publication existante
@login_required
def updatePost(request, pk):
    post = Posts.objects.get(id=pk)
    category = post.categorie
    form = PostForm(instance=post)
    context = {'form': form}

    # Vérifiez si l'utilisateur actuel est le créateur de la publication
    if post.user != request.user:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à modifier ce post.")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()

            return redirect(reverse(category))

    return render(request, 'posts/form_post.html', context)


# Vues pour afficher des publications dans différentes catégories
def restaurant(request):
    category = 'restaurant'
    category_param = request.GET.get('category')

    if category_param:
        category = category_param

    posts = Posts.objects.filter(categorie='restaurant').order_by('-created_at')
    category_count = Posts.objects.filter(categorie='restaurant').count()

    for post in posts:
        post.average_rating = Rating.objects.filter(post=post).aggregate(Avg('rating'))['rating__avg'] or 0
        post.rating_count = Rating.objects.filter(post=post).count()

    context = {
        'category': category,
        'posts': posts,
        'category_count': category_count,
    }
    return render(request, 'posts/restaurant_page.html', context)


def bar(request):
    category = 'bar'
    category_param = request.GET.get('category')

    if category_param:
        category = category_param

    posts = Posts.objects.filter(categorie='bar').order_by('-created_at')
    category_count = Posts.objects.filter(categorie='bar').count()

    for post in posts:
        post.average_rating = Rating.objects.filter(post=post).aggregate(Avg('rating'))['rating__avg'] or 0
        post.rating_count = Rating.objects.filter(post=post).count()

    context = {
        'category': category,
        'posts': posts,
        'category_count': category_count,
    }
    return render(request, 'posts/bar_page.html', context)


def tourisme(request):
    category = 'tourisme'
    category_param = request.GET.get('category')

    if category_param:
        category = category_param

    posts = Posts.objects.filter(categorie='tourisme').order_by('-created_at')
    category_count = Posts.objects.filter(categorie='tourisme').count()

    for post in posts:
        post.average_rating = Rating.objects.filter(post=post).aggregate(Avg('rating'))['rating__avg'] or 0
        post.rating_count = Rating.objects.filter(post=post).count()

    context = {
        'category': category,
        'posts': posts,
        'category_count': category_count,
    }
    return render(request, 'posts/tourism_page.html', context)


def nightClubs(request):
    category = 'nightClubs'
    category_param = request.GET.get('category')

    if category_param:
        category = category_param

    posts = Posts.objects.filter(categorie='nightClubs').order_by('-created_at')
    category_count = Posts.objects.filter(categorie='nightClubs').count()

    for post in posts:
        post.average_rating = Rating.objects.filter(post=post).aggregate(Avg('rating'))['rating__avg'] or 0
        post.rating_count = Rating.objects.filter(post=post).count()

    context = {
        'category': category,
        'posts': posts,
        'category_count': category_count,
    }
    return render(request, 'posts/night_clubs.html', context)
