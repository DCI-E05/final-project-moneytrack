from django.db import models
from django.contrib.auth.models import User
from categories.models import ExpensesCategory

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(ExpensesCategory, on_delete=models.CASCADE)
    amount = models.FloatField()
    description = models.TextField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Expense {self.name}"
