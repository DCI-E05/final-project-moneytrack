from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import FinanceData
from datetime import date

class FinanceDataAPITest(APITestCase):

    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a FinanceData object for testing
        self.finance_data = FinanceData.objects.create(
            user=self.user,
            account_number='12345',
            date=date(2023, 10, 4),
            details='Test Transaction',
            withdraw=100.0,
            deposit=200.0,
            balance=1000.0
        )

    def test_get_finance_data(self):
        # Test retrieving a FinanceData object via the API
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/upload/')  # Replace with your API endpoint URL
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Assuming it returns a list of FinanceData objects

    def test_create_finance_data(self):
        # Test creating a new FinanceData object via the API
        self.client.force_authenticate(user=self.user)
        data = {
            "user": self.user.id,
            "account_number": "54321",
            "date": "2023-10-05",
            "details": "New Transaction",
            "withdraw": 50.0,
            "deposit": 150.0,
            "balance": 1100.0
}

        response = self.client.post('/upload/file_upload/', data) 
        print(response.content)
# Use the full URL
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FinanceData.objects.count(), 2)  # Assuming a new object was created

    def test_update_finance_data(self):
        # Test updating an existing FinanceData object via the API
        self.client.force_authenticate(user=self.user)
        updated_data = {
            "deposit": 300.0,
            "balance": 1200.0
        }
        response = self.client.put(f'/upload/{self.finance_data.id}/', updated_data, format='json')  # Use the full URL
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.finance_data.refresh_from_db()  # Refresh the object from the database
        self.assertEqual(self.finance_data.deposit, 300.0)
        self.assertEqual(self.finance_data.balance, 1200.0)

    def test_delete_finance_data(self):
        # Test deleting a FinanceData object via the API
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/upload/{self.finance_data.id}/')  # Use the full URL
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(FinanceData.objects.count(), 0)
