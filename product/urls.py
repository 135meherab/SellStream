from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import Product, Order_create,Order_list,Customer_create,Customer_list,CustomerDelete,Uom_create,Uom_list,Category_create,Category_list


router = DefaultRouter()
router.register('',Product)

urlpatterns = [
    path('',include(router.urls)),
    path('order/', Order_create.as_view(), name='order-create'),
    path('order/list/', Order_list.as_view(), name='order-list'),
    path('customer/', Customer_create.as_view(), name='customer-create'),
    path('customer/list/', Customer_list.as_view(), name='customer-list'),
    path('customer/delete/<int:pk>/', CustomerDelete.as_view(), name='customer-delete'),
    path('uom/', Uom_create.as_view(), name='uom-create'),
    path('uom/list/', Uom_list.as_view(), name='uom-list'),
    path('category/', Category_create.as_view(), name='category-create'),
    path('category/list/', Category_list.as_view(), name='category-list'),
    # path('customer/<int:customer_id>/orders/', CustomerOrderHistoryAPIView.as_view(), name='customer_order_history_api'),
]