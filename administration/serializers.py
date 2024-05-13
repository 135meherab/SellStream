from rest_framework import serializers
from .models import AdminUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = ('email', 'fullname', 'phone', 'bio', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = AdminUser.objects.create_user(**validated_data)
        return user

class AdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)