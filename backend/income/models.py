from django.db import models
from django.contrib.auth.models import User
from categories.models import Category


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Define Category model before using it
    date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return f"{self.user.username}'s Income - {self.date}"


