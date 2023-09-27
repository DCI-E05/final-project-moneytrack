from rest_framework import viewsets
from django.contrib.auth import get_user_model
from .serializers import CustomerSerializer,ProfileSerializer
from .models import Profile



class CustomerViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = CustomerSerializer
    


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
      
    
    
    