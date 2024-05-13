from django.db import models
import json
from shop.models import Shop, Branch

# Create your models here.

class Customer(models.Model):
      shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
      name = models.CharField(max_length=50)
      phone = models.CharField(max_length=20, unique=True)
      total_purchase = models.DecimalField(max_digits=10, decimal_places=2)
      
      def __str__(self):
            return f"{self.name} - {self.phone}"


class Category(models.Model):
      uom_choice = (
            ('kg', 'Kilogram'),
            ('g', 'Gram'),
            ('l', 'Liter'),
            ('ml', 'Milliliter'),
            ('pcs', 'Pieces')
      )

      shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
      name = models.CharField(max_length=50)
      uom = models.CharField(max_length=10, choices=uom_choice)
      
      
      def __str__(self):
            return self.name


class Product(models.Model):
      branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
      category = models.ForeignKey(Category, on_delete=models.CASCADE)
      name = models.CharField(max_length=50)
      product_description = models.TextField()
      product_code = models.CharField(max_length=20, blank=True)
      buying_price = models.DecimalField(max_digits=10, decimal_places=2)
      selling_price = models.DecimalField(max_digits=10, decimal_places=2)
      quantity = models.IntegerField()
      store_date = models.DateField(auto_now_add=True)
      
      def save(self, *args, **kwargs):
            if not self.product_code:
                  last_product = Product.objects.last()
                  last_id = last_product.id if last_product else 0
                  category_prefix = self.category.name[0].upper()
                  product_prefix = self.name[:2].upper()
                  product_id = str(last_id + 1).zfill(5)
                  self.product_code = f"{category_prefix}{product_prefix}{product_id}"
            super().save(*args, **kwargs)
      
      def __str__(self):
            return self.name
      
      
class Order(models.Model):
      products = models.ManyToManyField(Product)
      customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
      branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
      order_unique_id = models.CharField(max_length=50)
      total_price = models.DecimalField(max_digits=10, decimal_places=2)
      order_date = models.DateField(auto_now_add=True)
      
      
      def __str__(self):
            return self.order_unique_id
      
      # # starting to store list of products data
      # products_json = models.TextField(default="[]", blank=False)
      
      # def get_products(self):
      #       return json.loads(self.products_json)
      
      # def set_products(self, products):
      #       self.products_json = json.dumps(products)
            
      # # ending to store list of products data


      # products = models.property(get_products, set_products)   #store a list of products
      
      

