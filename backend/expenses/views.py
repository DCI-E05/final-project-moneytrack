from rest_framework import viewsets
from rest_framework import permissions
from .serializers import ExpenseSerializer
from .models import Expense


class ExpensesViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Expense.objects.all()

    def get_queryset(self):
        user = self.request.user
        query_set = self.queryset
        return query_set.filter(user=user)

