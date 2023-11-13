from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from user_profile.models import UserProfile
from .models import Subscription
from .forms import CustomRegistrationForm
from django.contrib.auth.decorators import login_required


def register_verification(request):
    return render(request, 'register/register_verification.html')


from django.contrib.auth import authenticate, login

def verify_email(request, user_id, token):
    user = get_object_or_404(User, id=user_id)
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    subscription = user_profile.subscription

    if not subscription.email_verified and subscription.email_verification_token == token:
        subscription.email_verified = True
        subscription.save()


        user = authenticate(request, username=user.username, password=None)
        if user:
            login(request, user)

        messages.success(request, '¡Verificación exitosa!')
        return render(request, 'register/verification_success.html')
    else:
        messages.error(request, 'La verificación del correo electrónico no pudo completarse. El enlace puede haber expirado o ser inválido.')

    return render(request, 'register/verification_failure.html')


from django.contrib.auth import authenticate

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


            user_profile = UserProfile.objects.create(user=user, prenom=prenom, nom=nom)


            subscription = Subscription.objects.create(user=user_profile.user, first_name=prenom, last_name=nom)


            user_profile.subscription = subscription
            user_profile.save()


            return redirect('register_verification')

    else:
        form = CustomRegistrationForm()
    return render(request, 'register/register.html', {'form': form})
