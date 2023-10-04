from django.test import TestCase
from .models import FinanceData
from datetime import date

class FinanceDataModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        FinanceData.objects.create(
            account_number='12345',
            date='2023-10-04',
            details='Test Transaction',
            withdraw=100.0,
            deposit=200.0,
            balance=1000.0
        )

    def test_account_number_max_length(self):
        finance_data = FinanceData.objects.get(id=1)
        max_length = finance_data._meta.get_field('account_number').max_length
        self.assertEquals(max_length, 100)

    def test_balance_field_not_null(self):
        finance_data = FinanceData.objects.get(id=1)
        self.assertIsNotNone(finance_data.balance)

    def test_deposit_field_can_be_null(self):
        finance_data = FinanceData.objects.get(id=1)
        self.assertIsNone(finance_data.deposit)
    
    def test_withdraw_field_can_be_null(self):
        finance_data = FinanceData.objects.get(id=1)
        self.assertIsNone(finance_data.withdraw)


    def test_date_field_auto_now(self):
        finance_data = FinanceData.objects.get(id=1)
        # Check if the 'date' field is set to the current date
        self.assertIsNotNone(finance_data.date)
        self.assertEquals(finance_data.date, date(2023, 10, 4))

    def test_string_representation(self):
        finance_data = FinanceData.objects.get(id=1)
        expected_str = f"{finance_data.account_number} - {finance_data.date}"
        self.assertEquals(str(finance_data), expected_str)
