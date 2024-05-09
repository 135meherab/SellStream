from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, AdminLoginSerializer
from .models import AdminUser
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token


class AdminLoginApiview(APIView):
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(email=email, password=password)
            if user :
                login(request, user)
                return Response('successfully login ')
            else:
                return Response({'error': 'Invalid User'})

        return Response(serializer.errors)



class AdminLogoutAPIView(APIView):
    def get(self, request):
        logout(request)
        return Response('successfully logout')

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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