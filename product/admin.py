from django.contrib import admin
from .models import Category, Product, Customer, Order

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
      exclude = ['product_code']

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)