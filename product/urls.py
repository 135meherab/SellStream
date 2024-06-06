from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryAPIView, ProductAPIView, OrderListAPIView, CustomerListAPIView, RefundListAPIView

router = DefaultRouter()

router.register(r'categories', CategoryAPIView, basename='category')
router.register(r'products', ProductAPIView, basename='product')

urlpatterns = [
      path('', include(router.urls)),
      path('orders/', OrderListAPIView.as_view(), name='orders'),
      path('customer_list/', CustomerListAPIView.as_view(), name='customer_list'),
      path('refunds/', RefundListAPIView.as_view(), name='refunds'),
]
