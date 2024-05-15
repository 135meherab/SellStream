from rest_framework import serializers
from .models import DesignationModel, EmployeeModel, AttendanceModel, LeaveModel

class DesignationSerializers(serializers.ModelSerializer):
    class Meta:
        model = DesignationModel
        fields = '__all__'

class EmployeeSerializers(serializers.ModelSerializer):
    class Meta:
        model = EmployeeModel
        fields = '__all__'

class AttendanceSerializers(serializers.ModelSerializer):
    class Meta:
        model = AttendanceModel
        fields = '__all__'

class LeaveSerializers(serializers.ModelSerializer):
    class Meta:
        model = LeaveModel
        fields = '__all__'
