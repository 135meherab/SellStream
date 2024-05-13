from django.shortcuts import render
from rest_framework import viewsets
from .models import Category, Product, Customer, Order
from .serializers import CategorySerializer, ProductSerializer

# Create your views here.

class CategoryAPIView(viewsets.ModelViewSet):
      queryset = Category.objects.all()
      serializer_class = CategorySerializer
      
      
class ProductAPIView(viewsets.ModelViewSet):
      queryset = Product.objects.all()
      serializer_class = ProductSerializer
