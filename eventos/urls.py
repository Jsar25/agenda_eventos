# eventos/urls.py
from django.urls import path
from .views import home, crear_evento, registrar_evento, eliminar_evento

urlpatterns = [
    path('home/', home, name='home'),
    path('crear-evento/', crear_evento, name='crear_evento'),
    path('eventos/<int:evento_id>/eliminar/', eliminar_evento, name='eliminar_evento'),
    path('eventos/<int:evento_id>/registrar/', registrar_evento, name='registrar_evento')
]
