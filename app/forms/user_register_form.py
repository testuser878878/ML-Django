from django import forms
from django.contrib.auth.forms import UserCreationForm

from app.models import User


class UserRegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True, label='Роль')
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']
