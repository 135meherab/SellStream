from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework import viewsets
from .serializers import EmployeeSerializer, ShiftSerializer, DesignationSerializer, AttendanceSerializer
from .models import EmployeeDetailsModel, ShiftModel, DesignationModel, AttendanceModel
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins


# Create your views here.
class EmployeeViews(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    queryset = EmployeeDetailsModel.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class EmployeeView(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = EmployeeDetailsModel.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



class ShiftViews(ListCreateAPIView):
    queryset = ShiftModel.objects.all()
    serializer_class = ShiftSerializer
    permission_classes = [IsAuthenticated] 


class DesignationViews(viewsets.ModelViewSet):
    queryset = DesignationModel.objects.all()
    serializer_class = DesignationSerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset



class AttendanceViews(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    queryset = AttendanceModel.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class AttendanceView(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    queryset = AttendanceModel.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)



