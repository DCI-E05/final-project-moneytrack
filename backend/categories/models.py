from django.db import models
from django.contrib.auth.models import User


class IncomeCategories(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=255)
    description = models.TextField()

class ExpensesCategories(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=255)
    description = models.TextField()


