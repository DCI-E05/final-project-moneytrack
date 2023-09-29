from datetime import datetime
from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from categories.models import ExpensesCategory
from .models import Expense
import uuid


class ExpensesTest(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
                "username": "testUser",
                "email": "test@email.com",
                "password1": "123test123",
                "password2": "123test123"
            }
        self.user = self.client.post("/customer/rest-auth/registration/", data=self.user_data, format="json")
        self.client.post('/customer/rest-auth/login/', {"username": self.user_data["username"], "email": self.user_data['email'], "password": self.user_data['password1']})
        
        
    def test_creation(self):
        category_data = {
                "category_name": "test_category",
                "description": "My test category",
                "user": 1
            }
        category = self.client.post("/categories/expenses-category/", category_data).json()
        expense_data = {
                "name": "Test expence",
                "amount": 200.0,
                "date": datetime.now(tz=timezone.utc),
                "description": "My test expense description",
                "user": 1,
                "category": category['id']
            }
        expense = self.client.post("/expenses/", expense_data).json()
        
        
        self.assertNotEqual(expense, None)
        self.assertEqual(expense["name"], expense_data['name'])
        self.assertEqual(float(expense["amount"]), expense_data['amount'])
        self.assertEqual(expense["date"], expense_data['date'].strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        self.assertEqual(expense["description"], expense_data['description'])
        self.assertEqual(expense["user"], expense_data['user'])
        
        
    def test_retrieving(self):
        ...
        
    def test_update(self):
        ...
        
    def test_deletion(self):
        ...