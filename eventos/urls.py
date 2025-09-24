# eventos/urls.py
from django.urls import path
from .views import home, crear_evento, registrar_evento, eliminar_evento

urlpatterns = [
    # Quitamos la ruta raíz de aquí porque ya está en el urls.py principal
    path('crear-evento/', crear_evento, name='crear_evento'),
    path('<int:evento_id>/eliminar/', eliminar_evento, name='eliminar_evento'),
    path('<int:evento_id>/registrar/', registrar_evento, name='registrar_evento')
]
