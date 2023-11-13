from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.conf import settings

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30, blank=False, null=True)
    last_name = models.CharField(max_length=30, blank=False, null=True)
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, blank=True, null=True)
    user_profile = models.OneToOneField('user_profile.UserProfile', on_delete=models.CASCADE, null=True, blank=True, related_name='subscription_user_profile')

    @staticmethod
    def generate_verification_token():
        return get_random_string(50)

    def send_verification_email(self):
        subject = "SpotMyTown Vérification d'e-mail"
        message = f'Cliquez sur le lien suivant pour vérifier votre adresse e-mail:\n\n'
        message += f'{settings.BASE_URL}{reverse("verify_email", args=[str(self.user.id), self.email_verification_token])}'
        return subject, message

    def save(self, *args, **kwargs):
        if not self.email_verification_token:
            self.email_verification_token = self.generate_verification_token()
            subject, message = self.send_verification_email()
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [self.user.email],
                fail_silently=False,
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Abonnement de {self.user} - {self.first_name} {self.last_name}"
