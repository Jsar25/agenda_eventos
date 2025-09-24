from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from eventos.models import RegistroEvento, Evento
from .forms import EventoForm

@login_required
def home(request):
    user = request.user
    eventos = Evento.objects.all() #Esto sirve para traer todos los eventos

    context = {
        'user': user,
        'eventos': eventos
    }

    return render(request, 'eventos/home.html', context)

@login_required
def crear_evento(request):
    # Verificar que el usuario es administrador
    if request.user.rol != 'admin':
        messages.error(request, 'No tienes permisos para crear eventos.')
        return redirect('home')
    
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.creador = request.user  # Asignar el usuario actual como creador
            
            # Si no se proporciona fecha_fin, usar fecha_inicio + 1 hora
            if not evento.fecha_fin:
                evento.fecha_fin = evento.fecha_inicio + timedelta(hours=1)
            
            evento.save()
            messages.success(request, 'Evento creado exitosamente!')
            return redirect('home')
        else:
            # Agregar mensajes de error específicos para cada campo
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            return redirect('home')
    else:
        # Si es GET, redirigir a home (no debería pasar con modal)
        return redirect('home')

@login_required
def eliminar_evento(request, evento_id):
    # Verificar permisos de administrador
    if request.user.rol != 'admin':
        messages.error(request, 'No tienes permisos para eliminar eventos.')
        return redirect('home')
    
    # Solo permitir método POST
    if request.method == 'POST':
        try:
            evento = Evento.objects.get(id=evento_id)
            titulo_evento = evento.titulo
            evento.delete()
            messages.success(request, f'Evento "{titulo_evento}" eliminado exitosamente.')
            
            # Si es una solicitud AJAX, devolver JSON
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'ok', 'mensaje': f'Evento "{titulo_evento}" eliminado exitosamente.'})
                
        except Evento.DoesNotExist:
            messages.error(request, 'El evento no existe o ya fue eliminado.')
            
            # Si es una solicitud AJAX, devolver JSON con error
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'mensaje': 'El evento no existe o ya fue eliminado.'}, status=404)
    else:
        messages.error(request, 'Método no permitido para eliminar eventos.')
        
        # Si es una solicitud AJAX, devolver JSON con error
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'mensaje': 'Método no permitido para eliminar eventos.'}, status=405)
    
    return redirect('home')

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
