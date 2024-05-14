from django.shortcuts import render
from decimal import Decimal
from rest_framework import viewsets, generics, status, response, views
from .models import Category, Product, Customer, Order
from .serializers import CategorySerializer, ProductSerializer, CustomerSerializer, OrderSerializer


# Create your views here.

class CategoryAPIView(viewsets.ModelViewSet):
      queryset = Category.objects.all()
      serializer_class = CategorySerializer
      
      
class ProductAPIView(viewsets.ModelViewSet):
      queryset = Product.objects.all()
      serializer_class = ProductSerializer


class OrderCreateAPIView(views.APIView):      # use api view for the custom method
      def post(self, request, *args, **kwargs):
            print("request data: ", request.data)
            customer_serializer = CustomerSerializer(data=request.data['customer'])
            order_serializer = OrderSerializer(data=request.data.get('order'))
            
            customer_valid = customer_serializer.is_valid()
            order_valid = False
            

            if customer_valid:
                  customer_instance = customer_serializer.save()  # save the customer data

                  order_data = request.data.get("order", {})
                  order_data["customer"] = customer_instance.id
                  
                  print("order data: ", order_data)

                  order_serializer = OrderSerializer(data=order_data)
                  order_valid = order_serializer.is_valid()

            if customer_valid and order_valid:
                  order_instance = order_serializer.save()
                  
                  # convert total price into decimal
                  total_price_decimal = Decimal(order_instance.total_price)

                  # update the total purchase
                  customer_instance.total_purchase += total_price_decimal
                  customer_instance.save()

                  return response.Response(order_serializer.data, status=status.HTTP_201_CREATED)

            errors = {}
            if not customer_serializer.is_valid():
                  errors.update(customer_serializer.errors)
            if not order_serializer.is_valid():
                  errors.update(order_serializer.errors)
            return response.Response(errors, status=status.HTTP_400_BAD_REQUEST)



      def get(self, request, *args, **kwargs):
            order_queryset = Order.objects.all()
            order_serializer = OrderSerializer(order_queryset, many=True)
            return response.Response(order_serializer.data, status=status.HTTP_200_OK)


