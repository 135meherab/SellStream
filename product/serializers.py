from rest_framework import serializers
from .models import Category, Product, Customer, Order
from shop.models import Shop

class CategorySerializer(serializers.ModelSerializer):
      class Meta:
            model = Category
            fields = '__all__'
            read_only_fields = ['shop']
            
      def create(self, validated_data):
            request = self.context.get('request')
            
            # check the request is exist or not
            if request and hasattr(request.user, 'user'):
                  user = request.user
                  shop = user.shop
                  validated_data['shop'] = shop
            return super().create(validated_data)


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

      def get_branch_name(self, obj):
            return obj.branch.name if obj.branch else None

      def get_category_name(self, obj):
            return obj.category.name if obj.category else None



class CustomerSerializer(serializers.ModelSerializer):
      shop = serializers.PrimaryKeyRelatedField(
            queryset = Shop.objects.all(),
      )
      
      class Meta:
            model = Customer
            fields = ['name', 'phone', 'shop']



class OrderSerializer(serializers.ModelSerializer):
      customer = CustomerSerializer()
      
      class Meta:
            model = Order
            fields = '__all__'
            
            
      def create(self, validated_data):
            customer_data = validated_data.pop('customer')
            customer = Customer.objects.create(**customer_data)
            order = Order.objects.create(customer = customer, **validated_data)
            return order
            