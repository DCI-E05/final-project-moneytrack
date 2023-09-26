from .serializers import IncomeCategoriesSerializer, ExpensesCategoriesSerializer
from rest_framework.viewsets import ModelViewSet
from .models import IncomeCategories , ExpensesCategories


class IncomeCategoriesView(ModelViewSet):
    serializer_class = IncomeCategoriesSerializer
    queryset = IncomeCategories.objects.all()

class ExpensesCategoriesView(ModelViewSet):
    serializer_class = ExpensesCategoriesSerializer
    queryset = ExpensesCategories.objects.all()
