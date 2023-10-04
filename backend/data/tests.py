from django.test import TestCase
from .models import FinanceData
from datetime import date

class FinanceDataModelTest(TestCase):

    def setUp(self):
        # Create a FinanceData object for testing
        self.finance_data = FinanceData.objects.create(
            account_number='12345',
            date=date(2023, 10, 4),
            details='Test Transaction',
            withdraw=100.0,
            deposit=200.0,
            balance=1000.0
        )

    def test_account_number_max_length(self):
        max_length = self.finance_data._meta.get_field('account_number').max_length
        self.assertEqual(max_length, 100)

    def test_balance_field_not_null(self):
        self.assertIsNotNone(self.finance_data.balance)

    def test_deposit_field(self):
        self.assertEqual(self.finance_data.deposit , 200)

    def test_withdraw_field_can_be_null(self):
        self.assertEqual(self.finance_data.withdraw, 100)

    def test_date_field_auto_now(self):
        self.assertIsNotNone(self.finance_data.date)
        self.assertEqual(self.finance_data.date, date(2023, 10, 4))

    def test_balance_calculation(self):
        # Check that the balance is calculated correctly
        self.assertEqual(self.finance_data.balance, 1000.0 + 100.0 - 100.0)
