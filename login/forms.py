from django.contrib.auth.forms import AuthenticationForm
from django import forms

class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': (
            "Nom d'utilisateur ou mot de passe incorrect. Veuillez vérifier vos informations."
        ),
        'inactive': ("Ce compte est inactif."),
    }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.error_messages['__All__'] = None
