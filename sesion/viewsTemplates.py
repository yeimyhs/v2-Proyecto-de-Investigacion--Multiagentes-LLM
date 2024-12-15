from django.shortcuts import render
from rest_framework import generics

from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import *

from rest_framework import serializers

from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from knox.models import AuthToken


from django.shortcuts import render, get_object_or_404

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import JsonResponse

# Vista para mostrar la página de login o registro
def login_register_view(request):
    if request.user.is_authenticated:
        # Si ya está autenticado, redirigir al chat
        return redirect('companieroVirtual:chat_page')

    if request.method == 'POST':
        # Login
        if 'login' in request.POST:
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('companieroVirtual:chat_page')  # Redirigir al chat después de login exitoso
        # Registro
        elif 'register' in request.POST:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('sesion/login_register')  # Redirigir al login después de registro exitoso
        else:
            form = None
    else:
        form = None

    return render(request, 'sesion/login_register.html', {'form': form})

from django.views.decorators.clickjacking import xframe_options_exempt
@xframe_options_exempt
def session_detail_view(request, id):
    # Buscar la sesión por id o devolver error 404 si no existe
    session = get_object_or_404(Session, idsession=id)

    # Serializar la sesión usando el serializer
    serializer = SessionSerializer(session)

    # Devolver los datos serializados a la plantilla
    return render(request, 'sesion/session_detail.html', {'session': serializer.data})