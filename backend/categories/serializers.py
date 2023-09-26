from .models import IncomeCategories
from rest_framework import serializers
from .models import IncomeCategories, ExpensesCategories


class IncomeCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeCategories
        fields = '__all__'

class ExpensesCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpensesCategories
        fields = '__all__'