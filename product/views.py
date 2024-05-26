from django.shortcuts import render
from decimal import Decimal
from rest_framework import viewsets, generics, status, response, views, permissions, pagination, authentication
from .models import Category, Product, Customer, Order
from .serializers import CategorySerializer, ProductSerializer, CustomerSerializer, OrderSerializer

from rest_framework.pagination import PageNumberPagination

# Create your views here.

class CategoryAPIView(viewsets.ModelViewSet):
      permission_classes = [permissions.IsAuthenticated]
      authentication_classes = [authentication.TokenAuthentication]
      serializer_class = CategorySerializer
      
      def get_serializer_context(self):
            return {'request': self.request}
      
      def get_queryset(self):
            return Category.objects.filter(shop = self.request.user.shop).order_by('-id')
      
      
class ProductAPIView(viewsets.ModelViewSet):
      permission_classes = [permissions.IsAuthenticated]
      authentication_classes = [authentication.TokenAuthentication]
      pagination_class = pagination.PageNumberPagination
      serializer_class = ProductSerializer
      
      
      def get_queryset(self):
            user = self.request.user
            
            # By technically all products have a relation with a user
            if hasattr(user, 'shop'):
                  shop = user.shop
                  branches = shop.branch_set.all()
                  return Product.objects.filter(branch__in=branches).order_by('id')
            else:
                  return Product.objects.none()


class CustomerListAPIView(generics.ListCreateAPIView):
      permission_classes = [permissions.IsAuthenticated]
      authentication_classes = [authentication.TokenAuthentication]
      serializer_class = CustomerSerializer
      pagination_class = pagination.PageNumberPagination
      page_size = 10
      
      def get_queryset(self):
            user = self.request.user
            if hasattr(user, 'shop'):
                  shop =user.shop
                  return Customer.objects.filter(shop=shop).order_by('-id')
            else:
                  return Customer.objects.none()

class OrderListAPIView(generics.ListCreateAPIView):
      permission_classes = [permissions.IsAuthenticated]
      authentication_classes = [authentication.TokenAuthentication]
      serializer_class = OrderSerializer
      pagination_class = pagination.PageNumberPagination
      page_size = 10
      
      def get_queryset(self):
            user = self.request.user
            if hasattr(user, 'shop'):
                  shop = user.shop
                  branches = shop.branch_set.all()
                  return Order.objects_filter(branch__in = branches).order_by('-id')
            else:
                  return Order.objects.none()
            


# use api view for the custom method
class OrderCreateAPIView(views.APIView): 
      permission_classes = [permissions.IsAuthenticated]
      authentication_classes = [authentication.TokenAuthentication] 

      def post(self, request, *args, **kwargs):
            # Create the customer with authenticated user
            shop = request.user.shop
            customer_data = request.data.get('customer', {})
            customer_data['shop'] = shop.id
            customer_serializer = CustomerSerializer(data=customer_data)
            if customer_serializer.is_valid():
                  customer_instance = customer_serializer.save()
            else:
                  return response.Response(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # create the order with the created customer
            order_data = request.data.get('order', {})
            order_data['customer'] = customer_instance.id
            order_serializer = OrderSerializer(data=order_data)
            if order_serializer.is_valid():
                  order_instance = order_serializer.save()
                  return response.Response(order_serializer.data, status=status.HTTP_201_CREATED)
            else:
                  return response.Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

      # def post(self, request, *args, **kwargs):
      #       print("request data: ", request.data)
      #       customer_data = request.data.get('customer', {})
      #       phone_number  = customer_data.get('phone', None)
            
      #       # create or get customer based on phone number
      #       try:
      #             customer_instance = Customer.objects.get(phone = phone_number)
      #       except Customer.DoesNotExist:
      #             customer_serializer = CustomerSerializer(data=customer_data, context={'request': request})
      #             if customer_serializer.is_valid():
      #                   customer_instance = customer_serializer.save()
      #             else:
      #                   response.Response(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


      #       # create order if customer is valid
      #       if customer_instance:
      #             order_data = request.data.get('order', {})
      #             order_data['customer'] = customer_instance.id

      #             order_serializer = OrderSerializer(data=order_data)
      #       if customer_serializer.is_valid() and order_serializer.is_valid():
      #             order_instance = order_serializer.save()  # save the order data
                  
      #             # Handle product quantities
      #             products_data = request.data.get('products', [])
      #             for product_data in products_data:
      #                   product_id = product_data.get('product_id')
      #                   quantity = product_data.get('quantity', 1)
      #                   product = Product.objects.get(id=product_id)
      #                   if product.quantity >= quantity:
      #                         product.quantity -= quantity
      #                         product.save()
      #                   else:
      #                         return response.Response(f"Product {product.name} is out of stock", status=status.HTTP_400_BAD_REQUEST)
                        
      #                   order_instance.products.add(product, through_defaults={'quantity': quantity})

      #             # ensure the total price is a decimal
      #             total_price_decimal = Decimal(order_instance.total_price)

      #             # update the total purchase
      #             customer_instance.total_purchase += total_price_decimal
      #             customer_instance.save()

      #             return response.Response(order_serializer.data, status=status.HTTP_201_CREATED)
            
            
      #       return response.Response(order_serializer.is_valid(), status=status.HTTP_400_BAD_REQUEST)


      # def get(self, request, *args, **kwargs):
      #       paginator = pagination.PageNumberPagination()
      #       paginator.page_size = 10
      #       orders = Order.objects.all()
      #       result_page = paginator.paginate_queryset(orders, request)
      #       order_serializer = OrderSerializer(result_page, many=True)
      #       return paginator.get_paginated_response(order_serializer.data)



