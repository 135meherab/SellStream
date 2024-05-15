from django.shortcuts import render
from decimal import Decimal
from rest_framework import viewsets, generics, status, response, views, permissions
from .models import Category, Product, Customer, Order
from .serializers import CategorySerializer, ProductSerializer, CustomerSerializer, OrderSerializer


# Create your views here.

class CategoryAPIView(viewsets.ModelViewSet):
      permission_classes = [permissions.IsAuthenticated]
      queryset = Category.objects.all()
      serializer_class = CategorySerializer
      
      
class ProductAPIView(viewsets.ModelViewSet):
      permission_classes = [permissions.IsAuthenticated]
      queryset = Product.objects.all()
      serializer_class = ProductSerializer


class CustomerListAPIView(generics.ListCreateAPIView):
      permission_classes = [permissions.IsAuthenticated]
      queryset = Customer.objects.all()
      serializer_class = CustomerSerializer


class OrderListAPIView(generics.ListCreateAPIView):
      permission_classes = [permissions.IsAuthenticated]
      queryset = Order.objects.all()
      serializer_class = OrderSerializer


# use api view for the custom method
class OrderCreateAPIView(views.APIView):  
      permission_classes = [permissions.IsAuthenticated]
      
      
      def post(self, request, *args, **kwargs):
            print("request data: ", request.data)
            customer_data = request.data.get('customer', {})
            phone_number  = customer_data.get('phone', None)
            
            # create or get customer based on phone number
            try:
                  customer_instance = Customer.objects.get(phone = phone_number)
            except Customer.DoesNotExist:
                  customer_serializer = CustomerSerializer(data=customer_data)
                  if customer_serializer.is_valid():
                        customer_instance = customer_serializer.save()
                  else:
                        response.Response(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


            order_serializer = OrderSerializer(data=request.data.get('order'))
            customer_valid = True
            order_valid = False

            # create order if customer is valid
            if customer_instance:
                  order_data = request.data.get('order', {})
                  order_data['customer'] = customer_instance.id

                  order_serializer = OrderSerializer(data=order_data)
                  order_valid = order_serializer.is_valid()

            if customer_valid and order_valid:
                  order_instance = order_serializer.save()  # save the order data

                  # ensure the total price is a decimal
                  total_price_decimal = Decimal(order_instance.total_price)

                  # update the total purchase
                  customer_instance.total_purchase += total_price_decimal
                  customer_instance.save()

                  return response.Response(order_serializer.data, status=status.HTTP_201_CREATED)
            
            
            # All error message
            errors = {}
            if not customer_valid:
                  errors.update({'customer': 'Invalid customer data'})
            if not order_valid:
                  errors.update({'order': 'Invalid order data'})
            return response.Response(errors, status=status.HTTP_400_BAD_REQUEST)



      def get(self, request, *args, **kwargs):
            order_queryset = Order.objects.all()
            order_serializer = OrderSerializer(order_queryset, many=True)
            return response.Response(order_serializer.data, status=status.HTTP_200_OK)



