from django.urls import path
from rest_api.views import OrderDetail, OrderList, ItemList, ItemDetail, OrderItemList, OrderItemDetail, CustomerDetail, CustomerList, ItemFilter, OrderFilter, OrderCustomerFilter

urlpatterns = [
    path("orders/", OrderList.as_view()),
    path("orders/<int:pk>", OrderDetail.as_view()),
    path("items/", ItemList.as_view()),
    path("items/<int:pk>", ItemDetail.as_view()),
    path("items/search/", ItemFilter.as_view()),
    path("orders/sort/", OrderFilter.as_view()),
    path("orders-customer/", OrderCustomerFilter.as_view()),
    path("order-items/", OrderItemList.as_view()),
    path("order-items/<int:pk>", OrderItemDetail.as_view()),
    path("customers/", CustomerList.as_view()),
    path("customers/<int:pk>", CustomerDetail.as_view()),
]
