from rest_framework import serializers
from django.contrib.auth import get_user_model


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "username")
        model = get_user_model()

# serializers.py
from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'user', 'avatar')
        
        