import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agenda.settings')
import django
django.setup()
from usuarios.models import Usuario

if not Usuario.objects.filter(username='Juan').exists():
    Usuario.objects.create_user(
        username='Juan',
        password='123456',
        rol='estudiante'
    )
    print('Usuario Juan creado exitosamente')
else:
    print('El usuario Juan ya existe')