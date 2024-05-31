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
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework import viewsets
from datetime import datetime, timedelta
import random
import string


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
    queryset = Branch.objects.all()  # Initial queryset to fetch all Branch objects
    serializer_class = BranchSerializer

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    # Customizing the queryset based on the user role
    def get_queryset(self):
        user = self.request.user
        return Branch.objects.filter(shop__user=user)  # Else, return Branches related to the user's shop

    # Custom method to create a new Branch
    def perform_create(self, serializer):
        user = self.request.user
        shop = user.shop
        
        branch_name = serializer.validated_data['name']
        shop_name = shop.name
        
        # Generating username and password for the new branch user
        username = f"{shop_name}.{branch_name}".replace(" ", ".")
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        if User.objects.filter(username=username).exists():
            return Response({"message": "Branch already exists.Try to another branch name"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Creating a new user for the branch
            branch_user = User.objects.create_user(username=username, password=password)
        except Exception as e:
            return Response({"message": f"Failed to create user: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Saving the new branch with the associated user and shop
        serializer.save(user=branch_user, shop=shop)
        
        # Sending an email notification to the owner about the new branch
        email_subject = "New Branch Created"
        email_body = render_to_string('branch.html', {
            'user': user,
            'username': username,
            'password': password,
            'branch_name': branch_name,
            'shop_name': shop_name
        })
        
        try:
            # Sending the email
            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response({"message": "Successfully sent information"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": f"Failed to send email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

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
    def post(self, request):
        # Creating an instance of LoginSerializer with the request data
        serializer = LoginSerializer(data=self.request.data)
        
        # Checking if the serializer data is valid
        if serializer.is_valid():
            # Extracting username and password from validated data
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            # Authenticating the user with the provided credentials
            user = authenticate(username=username, password=password)
            if user:
                # Setting logout time 30 minutes from now
                logout_time = datetime.now() + timedelta(minutes=30)
                
                # Generating or retrieving existing token for the authenticated user
                token, created = Token.objects.get_or_create(user=user)
                
                # Logging in the user
                login(request, user)
                
                # Storing logout time in session
                request.session['logout_time'] = logout_time.strftime('%Y-%m-%d %H:%M:%S')

                # Constructing user_info dictionary based on user type
                user_info = {}
                if hasattr(user, 'branch'):
                    # User is a manager
                    user_info['role'] = 'isbranch'
                    user_info['username'] = user.username
                elif user.is_superuser:
                    # User is an admin
                    user_info['role'] = 'isadmin'
                    user_info['username'] = user.username
                    user_info['is_superuser'] = True
                else:
                    # User is an owner
                    user_info['role'] = 'isowner'
                    user_info['username'] = user.username
                    user_info['first_name'] = user.first_name
                    user_info['last_name'] = user.last_name
                    user_info['email'] = user.email

                # Returning response with token, user_id, logout_time, and user_info
                return Response({'token': token.key, 'user_id': user.id, 'logout_time': logout_time, 'user_info': user_info})
            else:
                # Returning error response for invalid credentials
                return Response({'error': "Invalid Credentials"})




class UserLogout(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get(self, request):
        if request.user.is_authenticated:
            try:
                request.user.auth_token.delete()
            except AttributeError:
                # User does not have an auth_token
                pass
            logout(request)
            return redirect('Login')
        else:
            return Response({'error': 'User is not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)
        
#get all user        
class UserDetailView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = DetailsSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # if user.is_staff:
        #     return User.objects.all()  # Admin can see all users
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

