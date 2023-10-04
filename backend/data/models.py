from django.db import models

# Create your models here.
class FinanceData(models.Model):
    account_number = models.CharField(max_length=100)
    date = models.DateField(auto_now=True)
    details = models.CharField( max_length=255)
    withdraw = models.FloatField(null=True)
    deposit = models.FloatField(null=True)
    balance = models.FloatField()
    
    
    def calculate_balance(self):
        self.balance = self.balance + self.deposit - self.withdraw
        self.save()