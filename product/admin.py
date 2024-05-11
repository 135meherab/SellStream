from django.contrib import admin
<<<<<<< HEAD

# Register your models here.
=======
from .models import Category, Uom, Customer, Product, Order

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',),}
    list_display = ['name','slug']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','description','product_code','quantity','price','category','uom_name']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['product_order','customer','quantity','Total','datetime']

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name','phone_no']



admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Uom)
admin.site.register(Customer,CustomerAdmin)
>>>>>>> c1d3c7f76dd2f2a4d6b3589fccf6c8b88f483f9a
