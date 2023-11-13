from django.shortcuts import render, redirect, get_object_or_404
from user_profile.forms import UserProfileForm
from user_profile.models import UserProfile
from django.contrib.auth.decorators import login_required



@login_required
def view_profile(request):
    # Récupère le profil de l'utilisateur actuellement connecté
    user_profile = get_object_or_404(UserProfile, user=request.user)
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


@login_required
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
