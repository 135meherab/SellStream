from rest_framework import serializers
from django.utils.text import slugify 
from .models import Category,Customer,Uom,Product, Order

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if 'name' in data and 'slug' not in data:
            data['slug'] = slugify(data['name'])
        return data

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class UomSerializers(serializers.ModelSerializer):
    class Meta:
        model = Uom
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','product_order','customer','quantity']

    def create(self, validated_data):
        product_order = validated_data['product_order']
        order_quantity = validated_data['quantity']
        price = product_order.price
        quantity = product_order.quantity
        quantity -= order_quantity
        product_order.save()
        total = quantity * price
        validated_data['Total'] = total
        return super().create(validated_data)

# class OrderDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order_Details
#         fields = '__all__'

