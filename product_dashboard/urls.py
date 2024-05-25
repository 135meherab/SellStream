from django.urls import path
from .views import sales_by_category


urlpatterns = [
      path('sales_by_category/', sales_by_category, name='sales_by_category'),
]