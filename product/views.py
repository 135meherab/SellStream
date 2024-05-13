from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListAPIView
from .models import Category,Customer,Product, Order
from .serializers import CustomerSerializer,ProductSerializers,OrderSerializer
from rest_framework.viewsets import ModelViewSet
# Create your views here.

class CreateProduct(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

# class Uom_create(CreateAPIView):
#     queryset = Uom.objects.all() # Specify the serializer class
#     serializer_class = UomSerializers
    
# class Uom_list(ListAPIView):
#     queryset = Uom.objects.all()
#     serializer_class = UomSerializers
    
# class Category_create(ModelViewSet): 
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
    
# class Category_list(ListAPIView):
#     queryset = Category.objects.all()
    

# class Customer_create(CreateAPIView):
#     serializer_class = CustomerSerializer  # Specify the serializer class
    
    
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid()
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    
# class Customer_list(ListAPIView):
#     queryset = Customer.objects.all()  # Specify the queryset to fetch all customers
#     serializer_class = CustomerSerializer  # Specify the serializer class for serialization

   
# class CustomerDelete(APIView):
#     def delete(self, request, pk):
#         try:
#             customer = get_object_or_404(Customer, pk=pk)
#             customer.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except Customer.DoesNotExist:
#             return Response({"error": "Customer does not exist."}, status=status.HTTP_404_NOT_FOUND)

# class Order_create(CreateAPIView):
#     serializer_class = OrderSerializer    # Specify the serializer class

#     def get_queryset(self):
#         # This method should return the queryset that the view will operate on
#         return Order.objects.all() 
    
#     def create(self,request,*args,**kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid()
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    
# class Order_list(ListAPIView):
#     queryset = Order.objects.all()  # Specify the queryset to fetch all customers
#     serializer_class = OrderSerializer  # Specify the serializer class for serialization

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         customer_id = self.request.query_params.get('customer_id')
#         if customer_id:
#             queryset = queryset.filter(customer_id=customer_id)
#         return queryset
    

    









# class CustomerOrderHistoryAPIView(ListAPIView):
#     serializer_class = OrderSerializer
#     def get_queryset(self):
#         customer_id = self.kwargs['customer_id']
#         try:
#             customer = Customer.objects.get(pk=customer_id)
#             return Order.objects.filter(customer=customer)
#         except Customer.DoesNotExist:
#             return []