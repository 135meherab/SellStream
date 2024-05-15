from rest_framework import serializers
from .models import Category, Product, Customer, Order

class CategorySerializer(serializers.ModelSerializer):
      class Meta:
            model = Category
            fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
      class Meta:
            model = Product
            
      def to_representation(self, instance):
            data = super().to_representation(instance)
            request = self.context.get('request')  # check the requested method
            
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