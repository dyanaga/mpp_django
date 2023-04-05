from rest_framework import generics
from rest_framework.exceptions import ValidationError

from rest_api.models import *
from django.db.models import Avg, OuterRef, Max, Sum, F, Subquery, Q, Count
from rest_api.serializers import *


class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer_basic

    def perform_create(self, serializer):
        serializer.save()


class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


# class OrderFilter(generics.ListAPIView):
#     serializer_class = OrderSerializer
#


class CustomerList(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def perform_create(self, serializer):
        serializer.save()


class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class ItemList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def perform_create(self, serializer):
        serializer.save()


class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class OrderItemList(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer_basic

    def perform_create(self, serializer):
        serializer.save()


class OrderItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class ItemFilter(generics.ListAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            queryset = Item.objects.all()
            price_greater = self.request.GET.get('q', None)
            print(f"greater than {price_greater}")
            try:
                if price_greater is not None:
                    quantity_greater = int(price_greater)
                    price = Item.objects.aggregate(Avg('price'))["price__avg"]
                    print("avg price: ", price)
                    price += quantity_greater
                    print("avg price + price: ", price)
                    queryset = Item.objects.filter(price__gt=price)

            except TypeError:
                pass
            return queryset


class OrderFilter(generics.ListAPIView):
    serializer_class = OrderFilterSerializer

    def get_queryset(self):
        return Order.objects.annotate(total=Sum(OrderItem.objects.filter(order__id=OuterRef("pk")).values("total"))).order_by("total")


class OrderCustomerFilter(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        query = Order.objects.annotate(name=Customer.objects.filter(id=OuterRef("pk")).values("name")).order_by("name")
        return query
