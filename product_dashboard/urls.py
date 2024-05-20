from django.urls import path
from .views import inventory_analysis_monthly


urlpatterns = [
      path('inventory_monthly/', inventory_analysis_monthly, name='inventory_monthly'),
]