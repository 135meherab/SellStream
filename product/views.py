from django.shortcuts import render
from rest_framework import viewsets
from .models import Category,Customer,Uom,Product, Order
from .serializers import CategorySerializer,CustomerSerializer,UomSerializers,ProductSerializer,OrderSerializer
# Create your views here.

class ProductAdd(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# class product_order()