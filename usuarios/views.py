from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.shortcuts import redirect

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'

    def get_success_url(self):

        return '/home/'