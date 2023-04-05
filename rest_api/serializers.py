from django.db.models import Sum
from rest_framework import serializers
from rest_api.models import *


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class OrderItemSerializer_basic(serializers.ModelSerializer):
    item_id = serializers.IntegerField(write_only=True)
    order_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    total = serializers.IntegerField(required=False)

    def validate_item_id(self, value):
        filter = Item.objects.filter(id=value)
        if not filter.exists():
            raise serializers.ValidationError("Item does not exist")
        return value

    def validate_order_id(self, value):
        filter = Order.objects.filter(id=value)
        if not filter.exists():
            raise serializers.ValidationError("Order does not exist")
        return value

    class Meta:
        model = OrderItem
        fields = ("id", "item_id", "order_id", "quantity", "total")


class OrderSerializer_basic(serializers.ModelSerializer):
    customer_id = serializers.IntegerField(write_only=True)
    status = serializers.CharField()
    payment_type = serializers.CharField()
    awb = serializers.CharField()

    def _get_qs_order_items_with_id(self, order):
        return_value = OrderItem.objects.filter(order=order)
        print(return_value)
        return return_value

    def validate_customer_id(self, value):
        filter = Customer.objects.filter(id=value)
        if not filter.exists():
            raise serializers.ValidationError("Customer does not exist")
        return value

    class Meta:
        model = Order
        fields = ("id", "customer_id", "status", "payment_type", "awb")


class OrderItemSerializer(OrderItemSerializer_basic):
    item = ItemSerializer(read_only=True)
    order = OrderSerializer_basic(read_only=True)

    class Meta:
        model = OrderItem
        fields = ("id", "item", "order", "quantity", "total")


class OrderSerializer(OrderSerializer_basic):
    order_items = serializers.SerializerMethodField()
    name = serializers.CharField(read_only=True)
    # customer = CustomerSerializer(read_only=True)

    def get_order_items(self, order):
        qs = self._get_qs_order_items_with_id(order)
        serializer = OrderItemSerializer_basic(instance=qs, many=True, read_only=True)
        return serializer.data

    class Meta:
        model = Order
        fields = ("id", "name", "customer_id", "status", "payment_type", "awb", "order_items")


class OrderFilterSerializer(OrderSerializer):
    # total = serializers.SerializerMethodField()
    total = serializers.IntegerField(read_only=True)

    # def get_total(self, order):
    #     qs = self._get_qs_order_items_with_id(order).aggregate(Sum("total"))["total__sum"]
    #     if qs is None:
    #         qs = 0
    #     return qs

    class Meta:
        model = Order
        fields = ("id", "customer_id", "status", "total", "payment_type", "awb", "order_items")
