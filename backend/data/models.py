from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class FinanceData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True,blank=True)
    account_number = models.CharField(max_length=100)
    date = models.DateField(auto_now=True)
    details = models.CharField( max_length=255)
    withdraw = models.FloatField(null=True)
    deposit = models.FloatField(null=True)
    balance = models.FloatField()
    
    
    def calculate_balance(self):
        return  self.balance + self.deposit - self.withdraw
