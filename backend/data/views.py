from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import FileUploadSerializer, FinanceDataSerializer
from .models import FinanceData
from rest_framework.pagination import PageNumberPagination
import os




class FileUploadView(viewsets.ViewSet):
    def create(self, request, format=None):
        serializer = FileUploadSerializer(data=request.data)

        if serializer.is_valid():
            uploaded_file = serializer.validated_data['file']
            file_directory = 'your_custom_file_directory/'
            file_path = os.path.join(file_directory, uploaded_file.name)

            if not os.path.exists(file_directory):
                os.makedirs(file_directory)
                


            with open(file_path, 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            return Response({'message': 'File uploaded and processed successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FinanceDataView(viewsets.ModelViewSet):
    queryset = FinanceData.objects.all()
    serializer_class = FinanceDataSerializer
    pagination_class = PageNumberPagination


class FinanceDataListView(generics.ListAPIView):
    queryset = FinanceData.objects.all()
    serializer_class = FinanceDataSerializer


class FinanceDataDetailView(generics.RetrieveAPIView):
    queryset = FinanceData.objects.all()
    serializer_class = FinanceDataSerializer
