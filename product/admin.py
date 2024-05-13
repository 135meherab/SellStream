from django.contrib import admin


# Register your models here.

from .models import Category, Customer, Product, Order

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','description','product_code','quantity','price','category']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['product_order','customer','quantity','Total','datetime']

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name','phone_no']



admin.site.register(Product,ProductAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Customer,CustomerAdmin)

