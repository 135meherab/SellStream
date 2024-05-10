from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductAdd


router = DefaultRouter()
router.register('',ProductAdd)

urlpatterns = [
    path('',include(router.urls)),
]