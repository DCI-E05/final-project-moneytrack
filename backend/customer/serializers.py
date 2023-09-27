from rest_framework import serializers
from django.contrib.auth import get_user_model


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "username")
        model = get_user_model()




        
        