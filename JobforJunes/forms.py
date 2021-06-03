from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from JobforJunes.models import User


class Register_User_Form(forms.ModelForm):
    class Meta:
        model=User
        fields=('name', 'email')



