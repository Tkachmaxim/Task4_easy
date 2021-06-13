from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from users_app.forms import RegisterUserForm


class MySignupView(CreateView):
    form_class = RegisterUserForm
    success_url = '/login'
    template_name = r'register/signup.html'


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = r'register/login.html'
