from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User

#sustainability/forms.py

class LoginForm(AuthenticationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    account_type = forms.ChoiceField(choices=User.ACCOUNT_TYPES, required=True, help_text='Required. Select your account type.')

    class Meta:
        model = User
        fields = ['email', 'password', 'account_type']
