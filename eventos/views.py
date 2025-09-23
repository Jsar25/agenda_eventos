from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from eventos.models import RegistroEvento
from eventos.models import Evento
from django.contrib.auth.models import User


def home(request):
    user = request.user
    eventos = Evento.objects.all() #Esto sirve para traer todos los eventos

    context = {
        'user': user,
        'eventos': eventos
    }

    return render(request, 'home.html', context)



@csrf_exempt
def registrar_evento(request, evento_id):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')

        try:
            evento = Evento.objects.get(id=evento_id)

            #Se verifica disponibilidad de cupos
            if evento.capacidad_num <= 0:
                return JsonResponse({'status': 'error',
                                     'mensaje': 'No hay cupos disponibles'
                }, status=400)

            # Guardar registro
            RegistroEvento.objects.create(
                evento=evento,
                nombre=nombre,
                correo=correo
            )

            evento.capacidad_num -= 1
            evento.save(update_fields=['capacidad_num'])

            # Enviar correo de confirmación
            asunto = f"Confirmación de registro: {evento.titulo}"
            mensaje = f"Hola {nombre},\n\nTe has registrado correctamente en el evento {evento.titulo}.\nFecha de inicio: {evento.fecha_inicio}\n¡Gracias por tu registro!"
            send_mail(asunto, mensaje, None, [correo], fail_silently=False)

            return JsonResponse({'status': 'ok', 'mensaje': 'Registro exitoso, correo enviado'})

        except Evento.DoesNotExist:
            return JsonResponse({'status': 'error', 'mensaje': 'Evento no encontrado'}, status=404)

    return JsonResponse({'status': 'error', 'mensaje': 'Método no permitido'}, status=405)
