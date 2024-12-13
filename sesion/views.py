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

from django.shortcuts import redirect

# Create your views here.
class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        
        if user is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        if not user.is_active:
            return Response({"error": "Account disabled"}, status=status.HTTP_403_FORBIDDEN)
        
        login(request, user)
        #return super(LoginView, self).post(request, format=None)
        return redirect('companieroVirtual:chat_page') 

    def throttled(self, request, wait):
        return Response(
            {"error": "Too many failed login attempts, please try again later"},
            status=status.HTTP_429_TOO_MANY_REQUESTS
        )
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "user": serializer.data,
            "token": AuthToken.objects.create(user)[1]
        })
        
        
class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.order_by('-pk')
    serializer_class = CustomUserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = [ 'email']
    filterset_fields = [ 'email']
