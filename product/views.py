
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, status, response, permissions, pagination, authentication
from django_filters import rest_framework as filters
from .models import Category, Product, Customer, Order, Refund
from .serializers import CategorySerializer, ProductSerializer, CustomerSerializer, OrderSerializer, RefundSerializer
from .filters import ProductFilter, OrderFilter
from shop.models import Branch

from rest_framework.pagination import PageNumberPagination

# Create your views here.

class CategoryAPIView(viewsets.ModelViewSet):
      permission_classes = [permissions.IsAuthenticated]
      authentication_classes = [authentication.TokenAuthentication]
      serializer_class = CategorySerializer
      
      def get_serializer_context(self):
            return {'request': self.request}
      
      def get_queryset(self):
            user = self.request.user
            
            # Check the user is shop or branch
            if hasattr(user, 'shop'):
                  return Category.objects.filter(shop = user.shop).order_by('-id')
            elif hasattr(user, 'branch'):
                  return Category.objects.filter(shop = user.branch.shop).order_by('-id')
            return Category.objects.none()
      
class ProductAPIView(viewsets.ModelViewSet):
      permission_classes = [permissions.IsAuthenticated]
      authentication_classes = [authentication.TokenAuthentication]
      pagination_class = pagination.PageNumberPagination
      serializer_class = ProductSerializer
      filter_backends = (filters.DjangoFilterBackend,)
      filterset_class = ProductFilter
      
      
      
      def get_queryset(self):
            user = self.request.user
            
            # Check the user is shop or branch
            if hasattr(user, 'shop'):
                  branches = user.shop.branches.all()
                  return Product.objects.filter(branch__in = branches).order_by('-id')
            elif hasattr(user, 'branch'):
                  return Product.objects.filter(branch = user.branch).order_by('-id')
            return Product.objects.none()
      
      
      # For creating and updating based on branch
      def perform_create(self, serializer):
            user = self.request.user
            if hasattr(user, 'branch'):
                  serializer.save(branch = user.branch)
            else:
                  serializer.save()
      
      
      def perform_update(self, serializer):
            user = self.request.user
            if hasattr(user, 'branch'):
                  serializer.save(branch = user.branch)
            else:
                  serializer.save()


class CustomerListAPIView(generics.ListAPIView):
      permission_classes = [permissions.IsAuthenticated]
      authentication_classes = [authentication.TokenAuthentication]
      serializer_class = CustomerSerializer
      pagination_class = pagination.PageNumberPagination
      page_size = 10
      
      def get_queryset(self):
            user = self.request.user
            
            # Check the user is shop or branch
            if hasattr(user, 'shop'):
                  return Customer.objects.filter(shop=user.shop).distinct().order_by('-id')
            elif hasattr(user, 'branch'):
                  # Filter customers who have orders in the specific branch
                  return Customer.objects.filter(
                              id__in = Order.objects.filter(branch = user.branch).values('customer_id')
                        ).order_by('-id')
            return Customer.objects.none()
            

class OrderListAPIView(generics.ListCreateAPIView):
      permission_classes = [permissions.IsAuthenticated]
      authentication_classes = [authentication.TokenAuthentication]
      filter_backends = (filters.DjangoFilterBackend,)
      filterset_class = OrderFilter
      serializer_class = OrderSerializer
      pagination_class = pagination.PageNumberPagination
      page_size = 10
      
      def get_queryset(self):
            user = self.request.user
            
            # Check the user is shop or branch
            if hasattr(user, 'shop'):
                  branches = user.shop.branches.all()
                  return Order.objects.filter(branch__in = branches).order_by('-id')

            elif hasattr(user, 'branch'):
                  return Order.objects.filter(branch = user.branch).order_by('-id')
            return Order.objects.none()



      def create(self, request, *args, **kwargs):
            serializer_context = {'request': request}
            user = request.user
            
            # Check the user is shop or branch
            if hasattr(user, 'shop'):
                  shop = user.shop
            elif hasattr(user, 'branch'):
                  shop = user.branch.shop
            else:
                  return response.Response({'detail': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)

            customer_data = request.data.get('customer', {})
            customer_phone = customer_data.get('phone')
            customer_data['shop'] = shop.id
            
            # Create customer or finding by phone
            try:
                  customer = Customer.objects.get(phone = customer_phone, shop = shop)
            except Customer.DoesNotExist:
                  customer_serializer = CustomerSerializer(data=customer_data)
                  if customer_serializer.is_valid():
                        customer = customer_serializer.save()
                  else:
                        return response.Response(
                                    customer_serializer.errors, 
                                    status=status.HTTP_400_BAD_REQUEST,
                              )                        
                        
            # Create order
            order_data = request.data
            order_data['customer'] = customer.id
            
            # If the user is in branch
            if hasattr(user, 'branch'):
                  order_data['branch'] = user.branch.id

            order_serializer = OrderSerializer(data=order_data, context = serializer_context)
            # print(order_serializer)
            if order_serializer.is_valid():
                  order = order_serializer.save()            
                  return response.Response(order_serializer.data, status=status.HTTP_201_CREATED)
            else:
                  return response.Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                  
                  
                  
class RefundListAPIView(generics.ListCreateAPIView):
      permission_classes = [permissions.IsAuthenticated]
      authentication_classes = [authentication.TokenAuthentication]
      serializer_class = RefundSerializer
      
      def get_queryset(self):
            user = self.request.user
            
            # Check the user is shop or branch
            if hasattr(user, 'shop'):
                  branches = user.shop.branch_set.all()
                  return Refund.objects.filter(order__branch__in = branches).order_by('-id')
            elif hasattr(user, 'branch'):
                  return Refund.objects.filter(order__branch = user.branch).order_by('-id')
            return Refund.objects.none()


      def create(self, request, *args, **kwargs):
            serializer = self.get_serializer(data = request.data)
            serializer.is_valid(raise_exception = True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return response.Response(
                  serializer.data,
                  status = status.HTTP_201_CREATED,
                  headers = headers
            )



