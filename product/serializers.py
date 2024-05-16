from rest_framework import serializers
from .models import Category, Product, Customer, Order

class CategorySerializer(serializers.ModelSerializer):
      class Meta:
            model = Category
            fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
      product_code = serializers.CharField(write_only=True)
      
      class Meta:
            model = Product
            fields = '__all__'
            
      
      # Ignore the product_code field when the request method is POST     
      def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            if self.context['request'].method == 'POST':
                  self.fields.pop('product_code')



      # show product code in get method
      def to_representation(self, instance):
            data = super().to_representation(instance)  # check the requested method

            if self.context['request'].method == 'GET':
                  data['product_code'] = instance.product_code
                  data['branch_name'] = instance.branch.name if instance.branch else None
                  data['category_name'] = instance.category.name if instance.category else None

            return data

      def get_branch_name(self, obj):
            return obj.branch.name if obj.branch else None

      def get_category_name(self, obj):
            return obj.category.name if obj.category else None



class CustomerSerializer(serializers.ModelSerializer):
      class Meta:
            model = Customer
            fields = '__all__'
            

      def save(self, **kwargs):
            validated_data = dict(self.validated_data)
            instance = Customer.objects.create(**validated_data)
            return instance


class OrderSerializer(serializers.ModelSerializer):
      class Meta:
            model = Order
            fields = '__all__'