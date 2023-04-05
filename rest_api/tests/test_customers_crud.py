from collections import OrderedDict
from unittest import TestCase
from rest_api.models import Customer
from rest_framework.test import APIRequestFactory, APITestCase
from rest_api.views import CustomerList

class CustomerListViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.count = 15
        for index in range(cls.count):
            Customer.objects.create(last_name=f"Georgescu{index}", first_name="Gigel", middle_name="Ionel")

    def test_url_exists(self):
        response = self.client.get("/api/customers/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/api/not-customers")
        self.assertEqual(response.status_code, 404)

    def test_get(self):
        response = self.client.get("/api/customers/")
        self.assertEqual(len(response.data), self.count)
        # print(response.data[0])
        for index, customer in enumerate(response.data):
            my_last_name = f"Georgescu{index}"
            my_name = f"Gigel Ionel {my_last_name}"
            my_customer = OrderedDict([("id", index+1),
                           ("first_name", "Gigel"),
                           ("last_name", my_last_name),
                           ("middle_name", "Ionel"),
                           ("name", my_name),
                           ("email", f"Gigel.{my_last_name}@email.com"),
                           ("address", f"{my_name}'s address")])
            self.assertEqual(my_customer, customer)
