from django.db import models, transaction
from shop.models import Shop, Branch

# Create your models here.

class Customer(models.Model):
      shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
      name = models.CharField(max_length=50)
      phone = models.CharField(max_length=20, unique=True)
      total_purchase = models.DecimalField(
                  max_digits=10, 
                  decimal_places=2, 
                  default=0.00, 
                  editable=True,
            )

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
                  last_product = Product.objects.last()   # get the last product id
                  last_id = last_product.id if last_product else 0    # check for the id is exist or not
                  category_prefix = self.category.name[0].upper()
                  product_prefix = self.name[:2].upper()
                  product_id = str(last_id + 1).zfill(5)
                  self.product_code = f"{category_prefix}{product_prefix}{product_id}"
            super().save(*args, **kwargs)
      
      def __str__(self):
            return f"{self.product_code} - {self.name}"


class Order(models.Model):
      products = models.ManyToManyField(Product)
      customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
      branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
      order_unique_id = models.CharField(max_length=50)
      total_price = models.DecimalField(max_digits=10, decimal_places=2)
      order_date = models.DateField(auto_now_add=True)


      def __str__(self):
            return f"{self.order_unique_id} - {self.order_date}"
      
      
      @transaction.atomic
      def save(self, *args, **kwargs):
            super().save(*args, **kwargs)
            self.update_product_quantities()

                  
      def update_product_quantities(self):
            for product in self.products.all():
                  if product.quantity >= 0:
                        product.quantity -= 1
                        product.save()
                  else:
                        raise ValueError(f"Insufficient quantity for product {product.name}")



