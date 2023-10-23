from channels.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from posts.models import UserProfile
from subscription.forms import CustomRegistrationForm


# Create your views here.
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
