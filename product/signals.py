from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver


from .models import Order, Customer
            

@receiver(post_save, sender = Order)
def update_customer_total_purchase(sender, instance, created, **kwargs):
      if created:
            customer = instance.customer
            customer.total_purchase += instance.total_price
            customer.save()
      