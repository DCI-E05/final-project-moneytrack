from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth.models import User 
from datetime import datetime, timezone
from categories.models import IncomeCategory
from income.models import Income  
from django.urls import reverse
from rest_framework import status


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



class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_user_login(self):
        response = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(response)

    def test_user_logout(self):
        # Log in the user first
        self.client.login(username='testuser', password='testpassword')

        # Perform the logout action
        response = self.client.get(reverse('logout'))  # Replace 'logout' with your logout URL name

        # Check if the user is redirected to a specific URL upon successful logout
        self.assertRedirects(response, reverse('login'))  # Repla


from django.contrib.auth import get_user

class AuthenticationCase(APITestCase):
    '''def test_login(self):
        
        self.assertFalse(get_user(self.client).is_authenticated())
        self.client.login(username='fred', password='secret')
        self.assertTrue(get_user(self.client).is_authenticated()) '''   

    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse("rest_register")
        data = {
            "username": "moneytrack",
           # "email": "tracker@gmail.com",
            "password1": "MyP@SwOrD",
            "password2": "MyP@SwOrD",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "moneytrack")


from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase


class AccountTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('income/', include('income.urls')),
    ]

    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        
        url = reverse('income-list')
        response = self.client.get(url, format='json')
        print(response.status_code)
       # self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        #self.assertEqual(response.status_code, status.HTTP_204_OK)
        self.assertEqual(len(response.data), 1)