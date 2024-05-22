from django.shortcuts import render
from decimal import Decimal
from rest_framework import viewsets, generics, status, response, views, permissions, pagination, authentication
from .models import Category, Product, Customer, Order
from .serializers import CategorySerializer, ProductSerializer, CustomerSerializer, OrderSerializer


# Create your views here.

class CategoryAPIView(viewsets.ModelViewSet):
      permission_classes = [permissions.IsAuthenticated]
      authentication_classes = [authentication.TokenAuthentication]
      queryset = Category.objects.all()
      serializer_class = CategorySerializer
      
      
class ProductAPIView(viewsets.ModelViewSet):
      permission_classes = [permissions.IsAuthenticated]
      authentication_classes = [authentication.TokenAuthentication]
      pagination_class = pagination.PageNumberPagination
      queryset = Product.objects.all().order_by('id')
      serializer_class = ProductSerializer


class CustomerListAPIView(generics.ListCreateAPIView):
      permission_classes = [permissions.IsAuthenticated]
      authentication_classes = [authentication.TokenAuthentication]
      pagination_class = pagination.PageNumberPagination
      queryset = Customer.objects.all().order_by('total_purchase')
      serializer_class = CustomerSerializer


class OrderListAPIView(generics.ListCreateAPIView):
      permission_classes = [permissions.IsAuthenticated]
      authentication_classes = [authentication.TokenAuthentication]
      pagination_class = pagination.PageNumberPagination
      queryset = Order.objects.all().order_by('id')
      serializer_class = OrderSerializer


# use api view for the custom method
class OrderCreateAPIView(views.APIView): 
      permission_classes = [permissions.IsAuthenticated]
      authentication_classes = [authentication.TokenAuthentication] 

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


            # create order if customer is valid
            if customer_instance:
                  order_data = request.data.get('order', {})
                  order_data['customer'] = customer_instance.id

                  order_serializer = OrderSerializer(data=order_data)
            if customer_serializer.is_valid() and order_serializer.is_valid():
                  order_instance = order_serializer.save()  # save the order data
                  
                  # Handle product quantities
                  products_data = request.data.get('products', [])
                  for product_data in products_data:
                        product_id = product_data.get('product_id')
                        quantity = product_data.get('quantity', 1)
                        product = Product.objects.get(id=product_id)
                        if product.quantity >= quantity:
                              product.quantity -= quantity
                              product.save()
                        else:
                              return response.Response(f"Product {product.name} is out of stock", status=status.HTTP_400_BAD_REQUEST)
                        
                        order_instance.products.add(product, through_defaults={'quantity': quantity})

                  # ensure the total price is a decimal
                  total_price_decimal = Decimal(order_instance.total_price)

                  # update the total purchase
                  customer_instance.total_purchase += total_price_decimal
                  customer_instance.save()

                  return response.Response(order_serializer.data, status=status.HTTP_201_CREATED)
            
            
            return response.Response(order_serializer.is_valid(), status=status.HTTP_400_BAD_REQUEST)



      def get(self, request, *args, **kwargs):
            paginator = pagination.PageNumberPagination()
            paginator.page_size = 10
            orders = Order.objects.all()
            result_page = paginator.paginate_queryset(orders, request)
            order_serializer = OrderSerializer(result_page, many=True)
            return paginator.get_paginated_response(order_serializer.data)



