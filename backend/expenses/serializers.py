from rest_framework import serializers
from rest_framework import permissions
from .models import Expence

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expence
        fields = '__all__'