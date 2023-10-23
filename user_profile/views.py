from django.shortcuts import render, redirect
from user_profile.forms import UserProfileForm
from user_profile.models import UserProfile


# Create your views here.

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
