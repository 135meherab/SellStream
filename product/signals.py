from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver


from .models import Order, Product, Refund
            

@receiver(post_save, sender = Order)
def update_customer_total_purchase(sender, instance, created, **kwargs):
      if created:
            customer = instance.customer
            customer.total_purchase += instance.total_price
            customer.save()
      

@receiver(m2m_changed, sender = Order.products.through)
def update_product_quantities(sender, instance, action, **kwargs):
      if action == 'post_add' and hasattr(instance, 'product_data'):
            for product_info in instance.product_data:
                  product = Product.objects.get(id = product_info['id'])
                  product.quantity -= product_info['quantity']
                  product.save()
                  
                  
                  
                  
@receiver(post_save, sender = Refund)
def product_quantities_and_customer_purchase_after_refund(sender, instance, created, **kwargs):
      if created:
            order = instance.order
            
            # Update product quantities
            for product in order.products.all():
                  product_order_quantity = order.products.through.objects.get(order_id = order.id, product_id = product.id).quantity
                  product.quantity += product_order_quantity
                  product.save()
                  
            
            # Update customer total purchase
            customer = order.customer
            customer.total_purchase -= order.total_price
            customer.save()
                  