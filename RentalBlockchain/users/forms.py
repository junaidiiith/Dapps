from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class SignUpForm(UserCreationForm):
    private_key = forms.CharField(max_length=64, validators=[RegexValidator(regex='^.{64}$', message='Length has to be 64', code='nomatch')])

    class Meta:
        model = User
        fields = ('username', 'private_key', 'password1', 'password2', )