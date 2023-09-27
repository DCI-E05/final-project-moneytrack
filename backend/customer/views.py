from rest_framework import viewsets
from django.contrib.auth import get_user_model
from .serializers import CustomerSerializer




class CustomerViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = CustomerSerializer
    


      
    
    
    