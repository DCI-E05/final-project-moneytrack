from django.test import TestCase
from django.contrib.auth.models import User 
from datetime import datetime, timezone
from categories.models import IncomeCategory
from income.models import Income  

class IncomeTestCase(TestCase):
    def setUp(self):
        self.date_aware = datetime.now(tz=timezone.utc)
        self.user = User.objects.create(username='testuser')
        self.category = IncomeCategory.objects.create(category_name='Test Category',user=self.user)
        self.income = Income.objects.create(user=self.user, name="Test Income", amount=100.0, category=self.category,
                                         date = self.date_aware,  description="Test Description" )

    def test_income_creation(self):
        saved_income = Income.objects.get(pk=self.income.pk)

        self.assertEqual(saved_income.user, self.user)
        self.assertEqual(saved_income.name, "Test Income")
        self.assertEqual(saved_income.amount, 100.0)
        self.assertEqual(saved_income.category, self.category)
        self.assertEqual(saved_income.date, self.date_aware )  
        self.assertEqual(saved_income.description, "Test Description")


    


