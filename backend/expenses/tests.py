from datetime import datetime
from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from categories.models import ExpensesCategory
from .models import Expense


class ExpensesTest(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
                "username": "testUser",
                "email": "test@email.com",
                "password1": "123test123",
                "password2": "123test123"
            }
    
        self.category_data = {
                "category_name": "test_category",
                "description": "My test category",
                "user": 1
            }
        
        self.expense_data = {
                "name": "Test expence",
                "amount": 200.0,
                "date": datetime.now(tz=timezone.utc),
                "description": "My test expense description",
                "user": 1,
                "category": 1
            }
        
        self.user = self.client.post("/customer/rest-auth/registration/", self.user_data)
        last_user_id = User.objects.last().id
        self.expense_data['user'] = last_user_id
        self.category_data['user'] = last_user_id
        
        self.category = self.client.post("/categories/expenses-category/", self.category_data).json()
        print(self.category)
        self.expense_data['category'] = ExpensesCategory.objects.last().id
        
        self.user = self.client.post('/customer/rest-auth/login/', {"username": self.user_data["username"], "email": self.user_data['email'], "password": self.user_data['password1']})

        
    def test_creation(self):
        expense = self.client.post("/expenses/", self.expense_data).json()
        
        self.assertEqual(expense["name"], self.expense_data['name'])
        self.assertEqual(float(expense["amount"]), self.expense_data['amount'])
        self.assertEqual(expense["date"], self.expense_data['date'].strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        self.assertEqual(expense["description"], self.expense_data['description'])
        self.assertEqual(expense["user"], self.expense_data['user'])
        
        
    def test_retrieving(self):
        self.client.post("/expenses/", self.expense_data)
        self.client.post("/expenses/", self.expense_data)
        self.client.post("/expenses/", self.expense_data)

        expenses = self.client.get("/expenses/").json()
        
        self.assertEqual(len(expenses), 3)
        
    def test_update(self):
        ...
        
    def test_deletion(self):
        ...