from django.db import models
from usuarios.models import Usuario

TIPOS_EVENTO = [
    ('conferencia', 'Conferencia'),
    ('taller', 'Taller'),
    ('capacitacion', 'Capacitación'),
    ]

class Evento(models.Model):
    
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    lugar = models.CharField(max_length=200)
    imagen_url = models.URLField(max_length=200, blank=True, null=True)
    tipo_evento = models.CharField(max_length=20, choices=TIPOS_EVENTO, default='conferencia')
    estado = models.CharField(max_length=1, choices=(  # Mantener el antiguo campo si es necesario
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ('F', 'Finalizado')
    ), default='A')
    capacidad_num = models.PositiveIntegerField()
    creador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.titulo} ({self.tipo_evento})"