# views.py
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from .models import Evento, RegistroEvento
from .forms import RegistroEventoForm

@require_POST
def registrar_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    form = RegistroEventoForm(request.POST)
    if form.is_valid():
        registro = form.save(commit=False)
        registro.evento = evento

        # opcional: evitar registros duplicados por correo en el mismo evento
        if RegistroEvento.objects.filter(evento=evento, correo=registro.correo).exists():
            return JsonResponse({'status': 'error', 'message': 'Ya estás registrado en este evento.'}, status=400)

        registro.save()

        # enviar correo (fail_silently True en dev; en prod manejar errores)
        try:
            send_mail(
                'Confirmación de registro',
                f'Hola {registro.nombre},\n\nTu registro en "{evento.titulo}" se ha recibido correctamente.\n\nGracias.',
                None,  # usa DEFAULT_FROM_EMAIL
                [registro.correo],
                fail_silently=True
            )
        except Exception:
            pass

        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
