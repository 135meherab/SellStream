from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, AdminLoginSerializer, ChangePasswordSerializer
from .models import AdminUser
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model


class AdminLoginApiview(APIView):
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(email=email, password=password)
            if user :
                login(request, user)
                return Response({'message' : 'successfully login '}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid email'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors)



class AdminLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get the user's token
        try:
            token = Token.objects.get(user=request.user)
        except Token.DoesNotExist:
            return Response({'error': 'User token not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Delete the token
        token.delete()

        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
    
    
    def get(self, request):
        logout(request)
        return Response('successfully logout')

class ProfileView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'data' :  serializer.data}, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data' :  serializer.data}, status=status.HTTP_200_OK )
        return Response({'error' : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            # Set new password
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    