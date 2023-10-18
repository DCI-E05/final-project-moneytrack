from rest_framework import serializers

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

from .models import FinanceData

class FinanceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceData
        fields = "__all__"