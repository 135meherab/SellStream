from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Category
from .serializers import CategorySerializers
from rest_framework import viewsets 

# Create your views here.

# Create your views here.
class CreateCategory(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers

