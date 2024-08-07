from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Shop,Branch

class CustomUserCreationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required = True)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password','confirm_password']

    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']

        if password != confirm_password:
            raise serializers.ValidationError({'error': "Password Dosen't Matched"})
        
        if User.objects.filter(username = username).exists():
            raise serializers.ValidationError({'error': "Username Already exits.Try to another username"})
            
        if User.objects.filter(email = email).exists():
            raise serializers.ValidationError({'error': "Email Already exits.Try to another email"})
        account = User(username = username,first_name = first_name,last_name = last_name, email = email)
        account.set_password(password)
        account.is_active = False
        account.save()

        return account


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 50)
    password = serializers.CharField(write_only=True)

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']  

class DetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['id', 'username', 'email', 'first_name', 'last_name']    


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['username', 'first_name', 'last_name','email']    

class BranchSerializer(serializers.ModelSerializer):
    shop = serializers.SerializerMethodField()
    class Meta:
        model = Branch
        fields = ['id', 'name', 'location', 'shop']
    
    # Custom method to get the shop's name
    def get_shop(self, obj):
        if isinstance(obj, Branch):
            return obj.shop.name
        else:
            return "Already have this Branch name  in a shop"

    def create(self, validated_data):
        # Correct the type and get the user associated with the request
        user = self.context['request'].user
        
        # Get the shop associated with the user
        shop = user.shop
        
        # Add the shop to the validated data before creating the branch
        validated_data['shop'] = shop
        
        # Create and return the branch
        return Branch.objects.create(**validated_data)

class ShopSerializer(serializers.ModelSerializer):
    # Representing the user field with a custom method
    user = serializers.SerializerMethodField()
    branches = BranchSerializer(many=True, read_only=True)
    class Meta:
        model = Shop
        fields = '__all__'

    # Custom method to get the user's full name
    def get_user(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    
    def create(self, validated_data):
        # Correct the type and get the user associated with the request
        user = self.context['request'].user
        return Shop.objects.create(user=user, **validated_data)
        

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({'confirm_password': "New passwords don't match."})

        user = self.context['request'].user
        if not user.check_password(data.get('old_password')):
            raise serializers.ValidationError({'old_password': 'Incorrect password.'})

        return data
    
class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, data):
        new_password = data.get('new_password')
        confirm_new_password = data.get('confirm_new_password')

        if new_password != confirm_new_password:
            raise serializers.ValidationError("The two password fields didn't match.")

        return data

