from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListAPIView
from .models import Category,Customer,Uom,Product, Order
from .serializers import CategorySerializer,CustomerSerializer,UomSerializers,ProductSerializer,OrderSerializer
# Create your views here.

class ProductAdd(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class order_create(CreateAPIView):
    serializer_class = OrderSerializer    # Specify the serializer class
    def create(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    
class order_list(ListAPIView):
    queryset = Order.objects.all()  # Specify the queryset to fetch all customers
    serializer_class = OrderSerializer  # Specify the serializer class for serialization
    
class Customer_create(CreateAPIView):
    serializer_class = CustomerSerializer  # Specify the serializer class
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
class Customer_list(ListAPIView):
    queryset = Customer.objects.all()  # Specify the queryset to fetch all customers
    serializer_class = CustomerSerializer  # Specify the serializer class for serialization
    
class CustomerDelete(APIView):
    def delete(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
            customer.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Customer.DoesNotExist:
            return Response({"error": "Customer does not exist."}, status=status.HTTP_404_NOT_FOUND)
        

class Uom_create(CreateAPIView):
    serializer_class = UomSerializers  # Specify the serializer class
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
class Uom_list(ListAPIView):
    queryset = Uom.objects.all()
    serializer_class = UomSerializers
    
class Category_create(CreateAPIView):
    serializer_class = CategorySerializer  # Specify the serializer class
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
class Category_list(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer