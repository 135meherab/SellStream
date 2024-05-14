from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryAPIView, ProductAPIView, OrderCreateAPIView

router = DefaultRouter()

router.register(r'categories', CategoryAPIView, basename='category')
router.register(r'products', ProductAPIView, basename='product')

urlpatterns = [
      path('', include(router.urls)),
      path('order/', OrderCreateAPIView.as_view(), name='order_create'),
]
