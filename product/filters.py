import django_filters
from django_filters import rest_framework as filters
from .models import Product, Order

class ProductFilter(filters.FilterSet):
      category = django_filters.NumberFilter(
            field_name='category__id',
            lookup_expr='exact'
      )
      branch = django_filters.NumberFilter(
            field_name='branch__id',
            lookup_expr='exact'
      )
      
      class Meta:
            model = Product
            fields = ['category', 'branch']
            
            
class OrderFilter(filters.FilterSet):
      order_date = django_filters.DateFilter(
            field_name='order_date',
            lookup_expr='exact'
      )
      branch = django_filters.NumberFilter(
            field_name='branch__id',
            lookup_expr='exact'
      )
      
      class Meta:
            model = Order
            fields = ['order_date', 'branch']
      
      