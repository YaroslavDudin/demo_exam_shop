# orders/urls.py
from django.urls import path
from .views import order_list, order_add, order_edit, order_delete

urlpatterns = [
    path('', order_list, name='order_list'),
    path('add/', order_add, name='order_add'),
    path('edit/<int:pk>/', order_edit, name='order_edit'),
    path('delete/<int:pk>/', order_delete, name='order_delete'),
]
