from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'

    def get_success_url(self):

        if self.request.user.rol == 'admin':
            return reverse_lazy('panel_admin')
        return reverse_lazy('calendario')