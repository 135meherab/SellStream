from rest_framework import serializers
from .models import DesignationModel, EmployeeModel, AttendanceModel, LeaveModel, SpecialOccasionModel

class DesignationSerializers(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    class Meta:
        model = DesignationModel
        fields = '__all__'

    def get_owner(self,obj):
        return obj.owner.name
    
    def create(self, validated_data):
        # Correct the type and get the user associated with the request
        user = self.context['request'].user

        # Get the shop associated with the user
        shop = user.shop
        
        # Set the owner field
        validated_data['owner'] = shop

        return DesignationModel.objects.create(**validated_data)
    

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

class SpecialOccasionSerializers(serializers.ModelSerializer):
    class Meta:
        model = SpecialOccasionModel
        fields = '__all__'

