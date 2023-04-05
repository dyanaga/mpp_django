from collections import OrderedDict

from rest_api.models import Order, Customer
from rest_framework.test import APITestCase


class OrderFilterTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.count = 4
        """
        id = models.IntegerField(primary_key=True)
        customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
        status = models.CharField(max_length=20)
        payment_type = models.CharField(max_length=20)
        awb = models.CharField(max_length=40)
        """
        Customer.objects.create(last_name=f"Georgescu", first_name="Gigel", middle_name="Ionel", name="Gigel Ionel Georgescu")
        Customer.objects.create(last_name=f"Georgescu", first_name="ZGigel", middle_name="Ionel", name="ZGigel Ionel Georgescu")
        Customer.objects.create(last_name=f"Georgescu", first_name="AGigel", middle_name="Ionel", name="AGigel Ionel Georgescu")
        Customer.objects.create(last_name=f"Georgescu", first_name="BGigel", middle_name="Ionel", name="BGigel Ionel Georgescu")

        Order.objects.create(customer_id=1, awb="1" * 15, status="shipped", payment_type="card")
        Order.objects.create(customer_id=2, awb="1" * 15, status="shipped", payment_type="card")
        Order.objects.create(customer_id=3, awb="1" * 15, status="shipped", payment_type="card")
        Order.objects.create(customer_id=4, awb="1" * 15, status="shipped", payment_type="card")

    def test_get(self):
        response = self.client.get("/api/orders-customer/")
        self.assertEqual(len(response.data), self.count)
        # print(response.data[0])
        names = ["AGigel Ionel Georgescu", "BGigel Ionel Georgescu", "Gigel Ionel Georgescu", "ZGigel Ionel Georgescu"]
        ids = [3, 4, 1, 2]
        for index, order in enumerate(response.data):
            print(order)
            my_order = OrderedDict([("id", ids[index]),
                                    ("name", names[index]),
                                    ("status", "shipped"),
                                    ("payment_type", "card"),
                                    ("awb", "1" * 15),
                                    ("order_items", [])])
            self.assertEqual(my_order, order)
