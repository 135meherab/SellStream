from django.shortcuts import render
from rest_framework import viewsets
from .serializers import EmployeeSerializer, ShiftSerializer, DesignationSerializer, AttendanceSerializer
from .models import EmployeeDetailsModel, ShiftModel, DesignationModel, AttendanceModel
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class EmployeeViews(viewsets.ModelViewSet):
    queryset = EmployeeDetailsModel.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated] 

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     name = self.request.query_params.get('name')
    #     if name:
    #         queryset = queryset.filter(first_name__icontains=name)
    #     return queryset

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     name = self.request.query_params.get('name')
    #     if name:
    #         queryset = queryset.filter(last_name__icontains=name)
    #     return queryset

class ShiftViews(viewsets.ModelViewSet):
    queryset = ShiftModel.objects.all()
    serializer_class = ShiftSerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

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

class AttendanceViews(viewsets.ModelViewSet):
    queryset = AttendanceModel.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        queryset = AttendanceModel.objects.all()
        employee_id = self.request.query_params.get('employee_id', None)
        date = self.request.query_params.get('date', None)

        # Filter queryset based on employee and date
        if employee_id is not None:
            queryset = queryset.filter(employee_id=employee_id)
        if date is not None:
            # date  format 'YYYY-MM-DD'
            queryset = queryset.filter(date__date=date)

        return queryset
