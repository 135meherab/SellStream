from django.shortcuts import render
from rest_framework import viewsets
from .models import DesignationModel, EmployeeModel, AttendanceModel, LeaveModel
from .serializers import DesignationSerializers, EmployeeSerializers, AttendanceSerializers, LeaveSerializers
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
# Create your views here.

# Designation
class DesignationViews(viewsets.ModelViewSet):
    queryset = DesignationModel.objects.all()
    serializer_class = DesignationSerializers
    permission_classes = [IsAuthenticated]

# Employee
class EmployeeViews(viewsets.ModelViewSet):
    queryset = EmployeeModel.objects.all()
    serializer_class = EmployeeSerializers
    permission_classes = [IsAuthenticated]


# Attendance
class Attendanceview(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = AttendanceModel.objects.all()
    serializer_class = AttendanceSerializers
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class AttendanceviewRetrive(GenericAPIView, RetrieveModelMixin):
    queryset = AttendanceModel.objects.all()
    serializer_class = AttendanceSerializers
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


# Employee leave view
class Leaveview(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = LeaveModel.objects.all()
    serializer_class = LeaveSerializers
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)