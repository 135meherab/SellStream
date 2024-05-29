from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from .serializers import CustomUserCreationSerializer, LoginSerializer,DetailsSerializer,PasswordChangeSerializer,UserUpdateSerializer,ShopSerializer,BranchSerializer
from .models import Shop,Branch
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, ListAPIView,UpdateAPIView
from rest_framework import viewsets
from datetime import datetime, timedelta
from .permissions import IsOwner



# create a shop
class ShopCreateView(CreateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Check if the user already has a shop
        existing_shop = Shop.objects.filter(user=request.user).exists()
        if existing_shop:
            return Response({"detail": "You already have a shop. You cannot create another one."}, status=400)
        return super().create(request, *args, **kwargs)

# get shop list
class ShopList(ListAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  # Assuming IsAuthenticated is sufficient

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:  # Assuming 'is_staff' indicates an admin user
            return Shop.objects.all()
        return Shop.objects.filter(user=user)

#update to shop
class ShopUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    serializers_class = ShopSerializer
    def put(self, request):
        shop = Shop.objects.get(user=request.user)
        serializer = ShopSerializer(instance=shop, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# create Branch,get,update,delete
class Branchviewset(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:        # Assuming 'is_staff' indicates an admin user
            return Branch.objects.all()  # Admin can see all branches
        return Branch.objects.filter(shop__user=user)  # Regular users can only see their own branches
    
    # def perform_create(self, serializer):
    #     # Associate the branch with the current user before saving
    #     serializer.save(shop__user=self.request.user)
    


class RegisterAPIView(APIView):
    serializer_class = CustomUserCreationSerializer
    def post(self, request):
        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"https://sellstream.onrender.com/shop/activate/{uid}/{token}/"
            email_subject = "Confirm Your mail"
            email_body = render_to_string('confirm_email.html',{'confirm_link' : confirm_link})
            email = EmailMultiAlternatives(email_subject,'',to=[user.email])
            email.attach_alternative(email_body,"text/html")
            email.send()
            messages.success(request, 'Registration successful. Check your mail for confirmation')
            # return redirect('login')
            return Response("Check your mail for confirmation")
        return Response(user_serializer.errors)
        
        
class EmailVerificationView(View):
    def get(self, request, uid64, token):
        try:
            uid = urlsafe_base64_decode(uid64).decode()
            user = User.objects.get(pk = uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Email verification successful. You can now log in.')
        else:
            messages.error(request, 'Email verification failed.')
        return redirect('Login')


class UserLogin(APIView):
    def post(self,request):
        serializer = LoginSerializer(data = self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username = username, password = password)
            if user:
                logout_time = datetime.now() + timedelta(minutes=30)
                token, created = Token.objects.get_or_create(user = user)
                login(request,user)
                request.session['logout_time'] = logout_time.strftime('%Y-%m-%d %H:%M:%S')
                return Response({'token' : token.key, 'user_id': user.id, 'logout_time' : logout_time})    
            else:
                return Response({'error': "Invalid Creadential"})
            
class UserLogout(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get(self, request):
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            logout(request)
            return redirect('Login')
        else:
            return Response({'error': 'User is not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)

#get all user        
class UserDetailView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = DetailsSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all()  # Admin can see all users
        return User.objects.filter(id=user.id)  # Regular users can only see their own Details


class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    serializers_class = UserUpdateSerializer
    def put(self, request):
        serializer = UserUpdateSerializer(instance=request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
