from django.shortcuts import render
from eventos.models import Evento

def home(request):
    user = request.user
    eventos = Evento.objects.all() #Esto sirve para traer todos los eventos

    context = {
        'user': user,
        'eventos': eventos
    }

    return render(request, 'home.html', context)