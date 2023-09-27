from django.shortcuts import render
from django.db import models
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from .serializers import UserSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer