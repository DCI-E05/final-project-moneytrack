from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import FileUploadSerializer

class FileUploadView(APIView):
   # parser_classes = (FileUploadParser,)

    def post(self, request, format=None):
        serializer = FileUploadSerializer(data=request.data)

        if serializer.is_valid():
            file = serializer.validated_data['file']
            print("Uploaded file")
            print(type(file))

            # Process the uploaded file here, for example, save it or call your existing management command

            return Response({'message': 'File uploaded and processed successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
