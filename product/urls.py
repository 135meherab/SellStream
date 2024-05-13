from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryAPIView, ProductAPIView

router = DefaultRouter()

router.register(r'categories', CategoryAPIView, basename='category')
router.register(r'products', ProductAPIView, basename='product')

urlpatterns = [
      path('', include(router.urls))
]