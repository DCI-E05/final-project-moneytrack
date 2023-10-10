from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Expense

class ExpensesViewSetTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.upload_receipt_url = reverse('expenses-upload-receipt')

    def test_upload_receipt_valid(self):
        with open('expenses/test_files/test_image.jpg', 'rb') as receipt_image:
            response = self.client.post(self.upload_receipt_url, {'receipt_image': receipt_image}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Expense receipt processed successfully.')

    def test_upload_receipt_invalid_file_type(self):
        with open('expenses/test_files/test_file.txt', 'rb') as invalid_file:
            response = self.client.post(self.upload_receipt_url, {'receipt_image': invalid_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid form submission.')
