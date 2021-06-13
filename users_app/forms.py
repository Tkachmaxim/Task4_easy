from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label='Имя')
    last_name = forms.CharField(max_length=30, label='Фамилия')
    email = forms.EmailField(label='Адрес электронной почты')

    class Meta:
        model = get_user_model()
        labels = {
            'username': 'Логин',
            'password1': 'Пароль',
            'password2': 'Повторите пароль'}
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')
