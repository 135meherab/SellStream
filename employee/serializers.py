from rest_framework import serializers
from . import models

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EmployeeDetailsModel
        fields = '__all__'

class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ShiftModel
        fields = '__all__'

class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DesignationModel
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttendanceModel
        fields = '__all__'

