from django.shortcuts import render
from rest_framework import generics
from .serializers import UserRegistrationSerializer
from .models import User

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer