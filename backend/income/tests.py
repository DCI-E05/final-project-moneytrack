from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime  
from categories.models import IncomeCategory
from income.models import Income  

class IncomeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')

    def tearDown(self):
        # Clean up test data after each test case
        User.objects.filter(username='testuser').delete()

    def test_income_creation(self):
        # Create an IncomeCategory associated with the user
        category = IncomeCategory.objects.create(
            category_name='Test Category',
            user=self.user
        )

        # Create an "aware" datetime object for the date
        date_aware = timezone.now()

        # Create an Income instance
        income = Income.objects.create(
            user=self.user,
            name="Test Income",
            amount=100.0,
            category=category,
           # date=datetime.now(),  # Use the "aware" datetime object
            description="Test Description"
        )

        # Retrieve the created income from the database
        saved_income = Income.objects.get(pk=income.pk)

        # Check if the fields were saved correctly
        self.assertEqual(saved_income.user, self.user)
        self.assertEqual(saved_income.name, "Test Income")
        self.assertEqual(saved_income.amount, 100.0)
        self.assertEqual(saved_income.category, category)
        #self.assertEqual(saved_income.date, datetime.now())  # Use the "aware" datetime object
        self.assertEqual(saved_income.description, "Test Description")

    def test_income_str_method(self):
        # Create an IncomeCategory associated with the user
        category = IncomeCategory.objects.create(
            category_name='Test Category',
            user=self.user
        )

        # Create an "aware" datetime object for the date
        date_aware = timezone.now()

        # Create an Income instance
        income = Income.objects.create(
            user=self.user,
            name="Test Income",
            amount=100.0,
            category=category,
            date=date_aware,  # Use the "aware" datetime object
            description="Test Description"
        )

        # Check the __str__ method output
        expected_str = f"Income Test Income - {category.category_name}"
        self.assertEqual(str(income), expected_str)
