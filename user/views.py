from django.shortcuts import render
from rest_framework import generics
from user.serializers import UserSerializer
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class LoginUserView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES