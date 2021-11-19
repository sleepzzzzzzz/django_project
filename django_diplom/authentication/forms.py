from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from django.db.models import Q

from django_diplom import settings

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, label='пароль')

    class Meta:
        model = User
        fields = ['email', 'avatar']
        labels = {

            'email': 'email'

        }


def clean_password2(self):
    if self.cleaned_data['password1'] != self.cleaned_data['password2']:
        raise ValidationError(
            'пароли должны совпадать'
        )
    return self.cleaned_data['password2']


def clean(self):
    user = User.objects.filter(
        email=self.cleaned_data['email']).first()
    if user:
        raise ValidationError('пользователь с такими учетными данными уже существует ')
    return super().clean()


class LoginForm(forms.Form):
    email_or_username = forms.CharField(label='email или имя пользователя')
    password = forms.CharField(label='пароль', widget=forms.PasswordInput)

    def clean(self):
        user = authenticate(
            email=self.cleaned_data['email_or_username'],
            username=self.cleaned_data['email_or_username'],
            password=self.cleaned_data['password']
        )
        if not user:
            raise ValidationError('Введенные данные не верны ')
        return self.cleaned_data
