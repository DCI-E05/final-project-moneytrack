from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from categories.models import IncomeCategory


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    category = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE)  # Define Category model before using it
    date = models.DateTimeField(default=datetime.now)
    description = models.TextField(default="Empty description")

    def __str__(self):
        return f"{self.user.username}'s Income - {self.date}"
    