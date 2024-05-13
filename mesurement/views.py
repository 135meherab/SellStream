from django.shortcuts import render, get_object_or_404
from .models import Mesurement
from .serializers import MesurementSerializers
from rest_framework import viewsets 
from rest_framework.generics import ListAPIView


# Create your views here.

# Create your views here.
class CreateMesurement(viewsets.ModelViewSet):
    queryset = Mesurement.objects.all()
    serializer_class = MesurementSerializers

class MesurementList(ListAPIView):
    queryset = Mesurement.objects.all()
    serializer_class = MesurementSerializers