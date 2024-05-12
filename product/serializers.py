from rest_framework import serializers
from django.utils.text import slugify 
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
        fields = ['id','product_order','customer','quantity']

    def create(self, validated_data):
        product_order = validated_data['product_order']
        order_quantity = validated_data['quantity']
        price = product_order.price
        available_quantity = product_order.quantity

        # Check if the order quantity exceeds the available quantity
        if order_quantity > available_quantity:
            raise serializers.ValidationError("Order quantity exceeds available quantity.")
        
        # Update the quantity of the ordered product
        product_order.quantity -= order_quantity
        product_order.save()

         # Calculate total price
        total = order_quantity * price
        validated_data['Total'] = total

        # Create the order
        return super().create(validated_data)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        # Calculate Total dynamically and add it to the serialized data
        total = instance.quantity * instance.product_order.price
        data['Total'] = total
        
        return data
    

# class OrderDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order_Details
#         fields = '__all__'

