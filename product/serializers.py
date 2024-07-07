from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from .models import Category, Product, Customer, Order, Refund
from shop.models import Shop

class CategorySerializer(serializers.ModelSerializer):
      shop_name = serializers.CharField(source = 'shop.name', read_only = True)
      
      class Meta:
            model = Category
            fields = ['id','name', 'uom', 'shop_name']
            
      def create(self, validated_data):
            request = self.context.get('request')
            
            # check the request is exist or not
            if request and hasattr(request.user, 'shop'):
                  shop = request.user.shop
                  validated_data['shop'] = shop
            else:
                  raise serializers.ValidationError('User does not have a shop.')
            return super().create(validated_data)
      
      
      # Make representation for get
      def to_representation(self, instance):
            data = super().to_representation(instance)
            if self.context['request'].method != 'GET':
                  del data['shop_name']
            return data


class ProductSerializer(serializers.ModelSerializer):
      product_code = serializers.CharField(required = False)
      
      class Meta:
            model = Product
            fields = '__all__'
            
      
      # Ignore the product_code field when the request method is POST     
      def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            request = self.context.get('request', None)
            
            if request and request.method == 'POST':
                  self.fields.pop('product_code')



      # show product code in get method
      def to_representation(self, instance):
            data = super().to_representation(instance)  # check the requested method
            request = self.context.get('request', None)

            if request and request.method == 'GET':
                  data['product_code'] = instance.product_code
                  data['branch_name'] = instance.branch.name if instance.branch else None
                  data['category_name'] = instance.category.name if instance.category else None
            return data

      # methods to find the relation with obj
      def get_branch_name(self, obj):
            return obj.branch.name if obj.branch else None

      def get_category_name(self, obj):
            return obj.category.name if obj.category else None
      
      
      # For creating and updating the product from branch
      def create(self, validated_data):
            request = self.context.get('request')
            user = request.user
            if hasattr(user, 'branch'):
                  validated_data['branch'] = user.branch
            return super().create(validated_data)
      
      
      def update(self, instance, validated_data):
            request = self.context.get('request')
            user = request.user
            if hasattr(user, 'branch'):
                  validated_data['branch'] = user.branch
            return super().update(instance, validated_data)



class CustomerSerializer(serializers.ModelSerializer):    
      shop_name = serializers.CharField(source = 'shop.name', read_only = True)       # get the shop name
      
      class Meta:
            model = Customer
            fields = ['name', 'phone', 'shop', 'shop_name', 'total_purchase']
            
      
      # make presentation on get
      def to_representation(self, instance):
            data = super().to_representation(instance)
            if self.context['request'].method != 'GET':
                  del data['shop_name']          # remove shop name for non-get requests
            return data
      


# For using the product dict
class ProductOrderSerializer(serializers.Serializer):
      id = serializers.IntegerField()
      quantity = serializers.IntegerField()

class OrderSerializer(serializers.ModelSerializer):
      products = ProductOrderSerializer(many = True)
      branch_name = serializers.CharField(source = 'branch.name', read_only = True)
      customer_name = serializers.CharField(source = 'customer.name', read_only = True)
      
      class Meta:
            model = Order
            fields = '__all__'
            read_only_fields = ['branch_name', 'customer_name']
            
      # Change representation for get
      def to_representation(self, instance):
            data = super().to_representation(instance)
            request = self.context.get('request')
            if request and request.method != 'GET':
                  del data['branch_name']
                  del data['customer_name']
            return data
      
      # Create the order
      def create(self, validated_data):
            products_data = validated_data.pop('products')
            insufficient_products = []
            
            
            # Check the product availability before creating the order
            for product_data in products_data:
                  product = Product.objects.get(id = product_data['id'])
                  if product.quantity < product_data['quantity']:
                        insufficient_products.append({
                              'name': product.name,
                              'available_quantity': product.quantity,
                        })
            
            # send the total of insufficient products
            if insufficient_products:
                  raise serializers.ValidationError({
                        'insufficient_products':[
                              f"{item['name']} (available:{item['available_quantity']})"
                              for item in insufficient_products
                        ]
                  })
            
            
            # Create the order
            order = Order.objects.create(**validated_data)
            

            for product_data in products_data:
                  product = Product.objects.get(id = product_data['id'])
                  order.products.add(product)
                  
                  # update the product quantity
                  product.quantity -= product_data['quantity']
                  product.save()
                  
                  
            return order
      
      
class RefundSerializer(serializers.ModelSerializer):
      class Meta:
            model = Refund
            fields = '__all__'
            read_only_fields = ['refund_date']
            
      def validate(self, data):
            order = data['order']
            refund_date = timezone.now().date()
            
            # check if the refund in 7 days
            if refund_date > order.order_date + timedelta(days = 7):
                  raise serializers.ValidationError(
                        'Refund request is beyond the 7-day limit.'
                  )
            
            return data

