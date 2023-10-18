from django.db.models import Q, Avg
from django.http import HttpResponseForbidden, Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import Posts, UserProfile, Comment, Rating
from .forms import PostForm, UserProfileForm, CustomRegistrationForm, CommentForm, PostRatingForm
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.decorators import login_required


# Vue pour la page d'accueil
def home(request):
    # Récupérer toutes les publications triées par date de création décroissante
    posts = Posts.objects.all().order_by('-created_at')
    context = {'posts': posts}
    return render(request, 'home/home.html', context)


# Vue pour afficher une publication individuelle
def post(request, pk):
    try:
        post = Posts.objects.get(pk=pk)
    except Posts.DoesNotExist:
        raise Http404("La publication n'existe pas")

    comments = Comment.objects.filter(post=post).order_by('-created_at')
    ratings = Rating.objects.filter(post=post)
    average_rating = ratings.aggregate(Avg('rating'))['rating__avg']
    rating_count = ratings.count()
    scale_min = 1
    scale_max = 5

    average_rating = max(scale_min, min(scale_max, average_rating or scale_min))
    average_star = int(average_rating)
    stars_css_class = "fa-star-checked" if average_star >= 1 else ""

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
            return redirect('post', pk=pk)
    else:
        form = PostRatingForm()
    return redirect('post', pk=pk, )


# Vues pour les commentaires
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


# Vue pour afficher un formulaire de création de publication
@login_required
def formulaire(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Ajouter l'utilisateur actuel au post
            categorie = post.categorie
            post.save()
            # Rediriger l'utilisateur vers la page de la catégorie appropriée
            return redirect(reverse(categorie))

    else:
        form = PostForm()

    context = {'form': form}
    return render(request, 'posts/form_post.html', context)


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
    form = PostForm(instance=post)
    context = {'form': form}

    # Vérifiez si l'utilisateur actuel est le créateur de la publication
    if post.user != request.user:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à modifier ce post.")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()

    return render(request, 'posts/form_post.html', context)


# Vues pour afficher des publications dans différentes catégories
def restaurant(request):
    posts = Posts.objects.filter(categorie='restaurant').order_by('-created_at')
    for post in posts:
        post.average_rating = Rating.objects.filter(post=post).aggregate(Avg('rating'))['rating__avg'] or 0
        post.rating_count = Rating.objects.filter(post=post).count()

    context = {'posts': posts}
    return render(request, 'posts/restaurant_page.html', context)


def bar(request):
    posts = Posts.objects.filter(categorie='bar').order_by('-created_at')
    for post in posts:
        post.average_rating = Rating.objects.filter(post=post).aggregate(Avg('rating'))['rating__avg'] or 0
        post.rating_count = Rating.objects.filter(post=post).count()

    context = {'posts': posts}
    return render(request, 'posts/bar_page.html', context)


def tourisme(request):
    posts = Posts.objects.filter(categorie='tourisme').order_by('-created_at')
    for post in posts:
        post.average_rating = Rating.objects.filter(post=post).aggregate(Avg('rating'))['rating__avg'] or 0
        post.rating_count = Rating.objects.filter(post=post).count()

    context = {'posts': posts}
    return render(request, 'posts/tourism_page.html', context)


def nightClubs(request):
    posts = Posts.objects.filter(categorie='nightClubs').order_by('-created_at')
    for post in posts:
        post.average_rating = Rating.objects.filter(post=post).aggregate(Avg('rating'))['rating__avg'] or 0
        post.rating_count = Rating.objects.filter(post=post).count()

    context = {'posts': posts}
    return render(request, 'posts/night_clubs.html', context)


# Vue pour l'inscription d'un nouvel utilisateur
def register(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            prenom = form.cleaned_data['prenom']
            nom = form.cleaned_data['nom']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = User.objects.create_user(first_name=prenom, last_name=nom, username=username, email=email,
                                            password=password)
            # Créer un profil pour l'utilisateur
            user_profile = UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('home')  # Redirigez l'utilisateur vers la page d'accueil après l'inscription réussie

    else:
        form = CustomRegistrationForm()
    return render(request, 'register/register.html', {'form': form})


# Vue pour la connexion de l'utilisateur
def custom_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'register/login.html', {'form': form})


# Vue pour la déconnexion de l'utilisateur
def custom_logout(request):
    logout(request)
    return redirect('home')


# Classe pour la vue personnalisée de réinitialisation du mot de passe
class CustomPasswordResetView(PasswordResetView):
    # Spécifie le modèle de la page de réinitialisation du mot de passe
    template_name = 'registration/password_reset_form.html'

    # Spécifie le modèle de l'e-mail envoyé pour réinitialiser le mot de passe
    email_template_name = 'registration/password_reset_email.html'

    # Spécifie le modèle de l'objet (sujet) de l'e-mail
    subject_template_name = 'registration/password_reset_subject.txt'

    # URL de redirection après une réinitialisation de mot de passe réussie
    success_url = '/password_reset/done/'


# Vue pour afficher le profil de l'utilisateur
def view_profile(request):
    # Récupère le profil de l'utilisateur actuellement connecté
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        # Si le formulaire est soumis en tant que POST
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            # Si le formulaire est valide, enregistre les données dans le profil
            form.save()
            return redirect('view_profile')  # Redirige l'utilisateur vers sa page de profil
    else:
        # Si la méthode est GET ou le formulaire est invalide, initialise le formulaire avec les données du profil
        form = UserProfileForm(instance=user_profile)
    return render(request, 'profile/profile.html', {'user_profile': user_profile, 'form': form})


# Vue pour éditer le profil de l'utilisateur
def edit_profile(request):
    # Récupère le profil de l'utilisateur actuellement connecté
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        # Si le formulaire est soumis en tant que POST
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            # Si le formulaire est valide, enregistre les données mises à jour dans le profil
            form.save()
            return redirect('view_profile')  # Redirige l'utilisateur vers sa page de profil
    else:
        # Si la méthode est GET ou le formulaire est invalide, initialise le formulaire avec les données du profil
        form = UserProfileForm(instance=user_profile)
    return render(request, 'profile/edit_profile.html', {'form': form})
