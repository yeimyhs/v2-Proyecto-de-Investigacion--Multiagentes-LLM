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

#from .serializers import *

from rest_framework import serializers

from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from knox.models import AuthToken




from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import render

def chat_page(request):
    if not request.user.is_authenticated:
        return redirect('sesion:register_log')  # Redirigir a la página de login si el usuario no está autenticado
    return render(request, 'chat.html')