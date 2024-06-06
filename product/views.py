from rest_framework import viewsets, generics, status, response, permissions, pagination, authentication
from django_filters import rest_framework as filters
from .models import Category, Product, Customer, Order
from .serializers import CategorySerializer, ProductSerializer, CustomerSerializer, OrderSerializer
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
            # check for swagger view
            if getattr(self, 'swagger_fake_view', False):
                  return Category.objects.none()
            
            return Category.objects.filter(shop = self.request.user.shop).order_by('-id')
      
      
class ProductAPIView(viewsets.ModelViewSet):
      permission_classes = [permissions.IsAuthenticated]
      authentication_classes = [authentication.TokenAuthentication]
      pagination_class = pagination.PageNumberPagination
      serializer_class = ProductSerializer
      filter_backends = (filters.DjangoFilterBackend,)
      filterset_class = ProductFilter
      
      
      
      def get_queryset(self):
            user = self.request.user
            
            # By technically all products have a relation with a user
            if hasattr(user, 'shop'):
                  shop = user.shop
                  branches = shop.branch_set.all()
                  return Product.objects.filter(branch__in=branches).order_by('-id')
            else:
                  return Product.objects.none()


class CustomerListAPIView(generics.ListAPIView):
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
      filter_backends = (filters.DjangoFilterBackend,)
      filterset_class = OrderFilter
      serializer_class = OrderSerializer
      pagination_class = pagination.PageNumberPagination
      page_size = 10
      
      def get_queryset(self):
            user = self.request.user
            if hasattr(user, 'shop'):
                  shop = user.shop
                  branches = shop.branch_set.all()
                  return Order.objects.filter(branch__in = branches).order_by('-id')
            else:
                  return Order.objects.none()
            
      def perform_create(self, serializer):
        # Get the current user making the request
        user = self.request.user
        # Find the Order linked to this user
        branch = Branch.objects.get(user=user)
        # Save the new Order, linking them to the branch
        serializer.save(branch=branch)

      def create(self, request, *args, **kwargs):
            serializer_context = {'request': request}
            shop = request.user.shop 
            customer_data = request.data.get('customer', {})
            customer_phone = customer_data.get('phone')
            customer_data['shop'] = shop.id
            
            # Create customer or finding by phone
            try:
                  customer = Customer.objects.get(phone = customer_phone)
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
            order_serializer = OrderSerializer(data=order_data)
            # print(order_serializer)
            if order_serializer.is_valid():
                  order = order_serializer.save()      
                        
                  return response.Response(
                              order_serializer.data, 
                              status=status.HTTP_201_CREATED,
                        )
            else:
                  return response.Response(
                              order_serializer.errors, 
                              status=status.HTTP_400_BAD_REQUEST,
                        )
