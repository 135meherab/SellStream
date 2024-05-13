from rest_framework import serializers
from .models import Category, Product, Customer, Order

class CategorySerializer(serializers.ModelSerializer):
      class Meta:
            model = Category
            fields = '__all__'
            

class ProductSerializer(serializers.ModelSerializer):
      class Meta:
            model = Product
            exclude = ['product_code']
            
      def to_representation(self, instance):
            data = super().to_representation(instance)
            request = self.context.get('request')  # check the requested method
            
            if request and request.method == 'GET':
                  data['product_code'] = instance.product_code
            
            return data