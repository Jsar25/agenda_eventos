# eventos/urls.py
from django.urls import path
from .views import home
from . import views

urlpatterns = [
    path('home/', home, name='home'),
    path('eventos/<int:evento_id>/registrar/', views.registrar_evento, name='registrar_evento')
]
