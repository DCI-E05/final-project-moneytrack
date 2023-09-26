from .models import Income
from .serializers import IncomeSerializer
from rest_framework import viewsets
from rest_framework import permissions

class IncomeViewSet(viewsets.ModelViewSet):
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Income.objects.all()

    def get_queryset(self):
        user = self.request.user
        query_set = self.queryset
        return query_set.filter(user=user)
