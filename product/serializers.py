from rest_framework import serializers
from .models import Category,Customer,Uom,Product, Order

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

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
        fields = '__all__'

# class OrderDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order_Details
#         fields = '__all__'

