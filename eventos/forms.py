from django import forms
from .models import Evento, RegistroEvento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['titulo', 'descripcion', 'fecha_inicio', 'fecha_fin', 'lugar', 'tipo_evento', 'capacidad_num', 'imagen_url']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título del evento'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción del evento'}),
            'fecha_inicio': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'fecha_fin': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'lugar': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lugar del evento'}),
            'tipo_evento': forms.Select(attrs={'class': 'form-control'}),
            'capacidad_num': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'imagen_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'URL de la imagen (opcional)'}),
        }

class RegistroEventoForm(forms.ModelForm):
    class Meta:
        model = RegistroEvento
        fields = ['nombre', 'correo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre completo'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tu@email.com'}),
        }
