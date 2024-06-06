from django.urls import path
from .views import sales_by_category, ShopReportView


urlpatterns = [
      path('sales_by_category/', sales_by_category, name='sales_by_category'),
      path('shop_report/', ShopReportView.as_view(), name='shop_report'),
]