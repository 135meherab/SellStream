from django.urls import path
from .views import inventory_report, product_report


urlpatterns = [
      path('inventory_report/', inventory_report, name='inventory_report'),
      path('product_report/', product_report, name='product_report')
]