from django.db.models.signals import m2m_changed, pre_save, post_save
from django.dispatch import receiver


from .models import Order, Customer
            

@receiver(pre_save, sender = Order)
def handle_customer(sender, instance, **kwargs):
      print('signals work')
      if not instance.customer_id:
            customer_phone = instance.customer.phone
            
            try:
                  customer = Customer.objects.get(phone = customer_phone)
            except Customer.DoesNotExist:
                  customer_name = instance.customer.name
                  branch_shop = instance.branch.shop 
                  customer = Customer.objects.create(
                        phone = customer_phone, 
                        name = customer_name, 
                        shop = branch_shop
                  )
            
            instance.customer = customer
            
            print(customer)
      
      
@receiver(post_save, sender = Order)
def update_customer_total_expenses(sender, instance, created, **kwargs):
      if not created:
            total_price = instance.total_price
            instance.customer.total_purchase += total_price
            instance.customer.save()
            

@receiver(m2m_changed, sender = Order.products.through)
def update_product_quantities(sender, instance, action, **kwargs):
      if action == 'post_add':
            instance.update_product_quantities()