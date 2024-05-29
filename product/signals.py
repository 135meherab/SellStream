from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver


from .models import Order, Customer

@receiver(m2m_changed, sender = Order.products.through)
def update_product_quantities(sender, instance, action, **kwargs):
      if action == 'post_add':
            instance.update_product_quantities()
            

@receiver(pre_save, sender = Order)
def handle_customer(sender, instance, **kwargs):
      customer_phone = instance.customer.phone
      
      try:
            customer = Customer.objects.get(phone = customer_phone)
      except Customer.DoesNotExist:
            customer = Customer.objects.create(
                  shop = instance.branch.shop,
                  phone = customer_phone,
                  name = instance.customer.name,
            )
            
      instance.customer = customer