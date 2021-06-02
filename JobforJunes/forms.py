from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class Register_User_Form(UserCreationForm):
    pass
    name=forms.CharField(max_length=30, label='Ваше имя')
    surname=forms.CharField(max_length=30, label='Ваша фамилия')
    email=forms.EmailField(label='email')



