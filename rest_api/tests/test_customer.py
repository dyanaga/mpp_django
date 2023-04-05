from django.test import TestCase
from rest_api.models import Customer

class CustomerModelTestcase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Customer.objects.create(last_name="Georgescu", first_name="Gigel", middle_name="Ionel")

    def test_string_method(self):
        customer = Customer.objects.get(first_name="Gigel")
        expected_name = f"Gigel Ionel Georgescu"
        self.assertEqual(str(customer), expected_name)

    def test_email_method(self):
        customer = Customer.objects.get(first_name="Gigel")
        expected_email = f"Gigel.Georgescu@email.com"
        self.assertEqual(str(customer.email), expected_email)

    def test_address_method(self):
        customer = Customer.objects.get(first_name="Gigel")
        expected_address = "Gigel Ionel Georgescu's address"
        self.assertEqual(str(customer.address), expected_address)
 