from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryAPIView, ProductAPIView, OrderListAPIView, CustomerListAPIView

router = DefaultRouter()

router.register(r'categories', CategoryAPIView, basename='category')
router.register(r'products', ProductAPIView, basename='product')

urlpatterns = [
      path('', include(router.urls)),
      # path('order_create/', OrderCreateAPIView.as_view(), name='order_create'),
      path('order_list/', OrderListAPIView.as_view(), name='order_list'),
      path('customer_list/', CustomerListAPIView.as_view(), name='customer_list'),
]
