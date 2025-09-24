"""
URL configuration for agenda project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from eventos.views import home, eliminar_evento  # Importar la vista eliminar_evento
from usuarios.views import CustomLoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

# Vista simple para redirigir a la página de inicio
def redirect_to_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
    path('eventos/<int:evento_id>/eliminar/', eliminar_evento, name='eliminar_evento'),  # URL directa para eliminar eventos
    path('eventos/', include('eventos.urls')),
    path('login/', CustomLoginView.as_view(), name='login'),
    # Cambiamos la URL raíz para que redirija al login cuando sea necesario
    path('', redirect_to_login, name='root'),
    path('home/', login_required(home), name='home'),
]
