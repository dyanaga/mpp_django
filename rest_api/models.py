from django.db import models
from django.utils import timezone


class Customer(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f"{self.first_name} {self.middle_name} {self.last_name}"
        if not self.email:
            self.email = f"{self.first_name}.{self.last_name}@email.com"
        if not self.address:
            self.address = f"{self.name}'s address"

        super(Customer, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


# class Store(models.Model):
#     name = models.CharField(max_length=255)
#     address = models.CharField(max_length=255)
#     contact_email = models.CharField(max_length=255)
#     contact_phone = models.CharField(max_length=30)
#
#     def __str__(self):
#         return f"{self.name} ({self.address})"
#

class Item(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.IntegerField()
    category = models.CharField(max_length=30, null=True)
    # image = models.ImageField(null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    id = models.IntegerField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    payment_type = models.CharField(max_length=20)
    awb = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.customer.name}"


class OrderItem(models.Model):
    id = models.IntegerField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        if not self.total:
            self.total = self.item.price * self.quantity

        super(OrderItem, self).save(*args, **kwargs)

    def __str__(self):
        # return f"{self.order.customer.name} - {self.item.name}: {self.quantity}"
        return f"{self.item.name}: {self.order.id}"
