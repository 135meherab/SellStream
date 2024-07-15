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
from .serializers import CustomUserCreationSerializer, LoginSerializer,DetailsSerializer,PasswordChangeSerializer,UserUpdateSerializer,ShopSerializer,BranchSerializer,PasswordResetSerializer
from .models import Shop,Branch
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes ,force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework import viewsets
from datetime import datetime, timedelta
from django.core.cache import cache
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from django.utils import timezone
import json
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
            return Response({"message": "You already have a shop. You cannot create another one."}, status=400)
        return super().create(request, *args, **kwargs)

# get shop list
class ShopList(ListAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  # Assuming IsAuthenticated is sufficient

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Shop.objects.all()  # Admin sees all shops
        else:
            return Shop.objects.filter(user=user) # Others see only their own shops

#update to shop
class ShopUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    serializers_class = ShopSerializer
    def put(self, request):
        shop = Shop.objects.get(user=request.user) # Get the shop related to the current user
        serializer = ShopSerializer(instance=shop, data=request.data)   # Create a serializer instance with the shop data from the request
        if serializer.is_valid():  # Check if the data provided is valid
            serializer.save() # Save the updated shop data
            return Response(serializer.data, status=status.HTTP_200_OK)  # Return the updated data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return errors if data is invalid


# create Branch,get,update,delete
class Branchviewset(viewsets.ModelViewSet):
    queryset = Branch.objects.all()  # Initial queryset to fetch all Branch objects
    serializer_class = BranchSerializer

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        user = self.request.user
        try:
            branch = Branch.objects.get(user = user)    # Try to find a branch linked to this user
            return Branch.objects.filter(id = branch.id) # If found, return this branch
        except Branch.DoesNotExist:
            try:
                shop = Shop.objects.get(user = user)   # If no branch is found, try to find a shop linked to this user
                return Branch.objects.filter(shop = shop)  # If found, return all branches of this shop
            except Shop.DoesNotExist:
                return Branch.objects.none() # return an empty queryset

    # Custom method to create a new Branch
    def perform_create(self, serializer):
        user = self.request.user
        shop = user.shop
        
        branch_name = serializer.validated_data['name'] # Get the name of the new branch from the request
        shop_name = shop.name   # Get the name of the shop
        
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
            return Response({"message": "Branch created successfully. User credentials sent to your email."}, status=status.HTTP_201_CREATED)
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
            confirm_link = f"https://sellstreams1.onrender.com/shop/activate/{uid}/{token}/"
            email_subject = "Confirm Your mail"
            email_body = render_to_string('confirm_email.html',{'confirm_link' : confirm_link})
            email = EmailMultiAlternatives(email_subject,'',to=[user.email])
            email.attach_alternative(email_body,"text/html")
            email.send()
            messages.success(request, 'Registration successful. Check your mail for confirmation')
            # return redirect('login')
            return Response({"message": "Registration successful. Check your email for confirmation"}, status=status.HTTP_201_CREATED)
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
            return redirect('https://sell-stream.netlify.app/login')
        else:
            messages.error(request, 'Email verification failed.')
        # Do not redirect to login page
        return HttpResponse('Email verification failed.')


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
                return Response({'error': "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




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

    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()  # Superuser can see all users
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
    

class PasswordResetview(APIView):
    def post(self,request):
        email = request.data.get('email') # Get the email from the request data
        try:
            # Check if the user exists in the database
            user = User.objects.get(email = email)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        otp = get_random_string(length = 6, allowed_chars = '0123456789')  # Generate a random 6-digit OTP

        # Encode the email and user ID for secure transmission
        email_encode = urlsafe_base64_encode(force_bytes(email))
        user_Id_encode = urlsafe_base64_encode(force_bytes(user.id))
        data  = {'email': email_encode, 'user_id': user_Id_encode}

        # Encode the data and OTP for secure storage
        encoded_data = urlsafe_base64_encode(force_bytes(json.dumps(data)))
        otp_encoded = urlsafe_base64_encode(force_bytes(otp))

        cache.set(f'otp_{otp_encoded}', encoded_data , timeout=120)  # Store OTP in cache with a timeout of 120 seconds

        # Send OTP email
        email_subject = 'Password Reset OTP'
        email_body = render_to_string('otp.html',{'otp': otp})
        email = EmailMultiAlternatives(email_subject,'',to=[user.email])
        email.attach_alternative(email_body,"text/html")
        email.send()

        request.session['email'] = email_encode  # Store email in session
        messages.success(request, 'OTP sent to your email.')
        return Response({'message': 'OTP sent to your email.'}, status=status.HTTP_200_OK)
    

    

class VerifyOTPView(APIView):
    def post(self, request):
        # Get OTP from request data
        otp = request.data.get('otp')
        otp_encoded = urlsafe_base64_encode(force_bytes(otp))

        email_encoded = request.session.get('email') # Retrieve email from session
        if not email_encoded:
            return Response({'error': 'Email not found in session.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Decode user ID from email
        decoded_user_id = urlsafe_base64_decode(email_encoded).decode()
        attempt_count_key = f'otp_attempt_{decoded_user_id}'
        attempt_count_encoded = urlsafe_base64_encode(force_bytes(attempt_count_key))
        attempt_count = cache.get(attempt_count_encoded, 0)
        
        # Check if maximum attempts reached
        if attempt_count == 2:
            return Response({'error': 'Exceeded maximum OTP attempts. Please try again later.'}, status=status.HTTP_403_FORBIDDEN)
        
        # Get the verified OTP data from the cache
        cached_data = cache.get(f'otp_{otp_encoded}')
        
        # Check if OTP is valid
        if not cached_data:
            # Increment attempt count and set timeout for attempts
            attempt_count += 1
            cache.set(attempt_count_encoded, attempt_count, timeout=300)  
            
            return Response({'error': 'Invalid OTP or OTP has expired.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # OTP is valid, reset attempt count and delete email from session
        cache.delete(attempt_count_key)
        del request.session['email']


        # Decode cached data
        data = json.loads(force_str(urlsafe_base64_decode(cached_data)))
        email = data['email']
        user_id = data['user_id']     

        # Store verified OTP in cache
        data = {'email': email, 'user_id': user_id}
        encoded_data = urlsafe_base64_encode(force_bytes(json.dumps(data)))
        email_encoded = urlsafe_base64_encode(force_bytes(email))
        cache.set(f'verified_otp_{email_encoded}', encoded_data, timeout=300)

        request.session['email'] = email_encoded # Store email in session
        

        return Response({'message': 'OTP verified successfully. You can now change your password.' }, status=status.HTTP_200_OK)
    
class PasswordChangeViews(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']

            # Get email from session and get verified OTP data from cache
            email = request.session.get('email')
            cached_data = cache.get(f'verified_otp_{email}')
            
            if not cached_data:
                # Return error if verified OTP data not found or expired
                return Response({'error': 'OTP verification not found or expired.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Decode verified OTP data
            decoded_data = json.loads(force_bytes(urlsafe_base64_decode(cached_data)))
            user_id = int(urlsafe_base64_decode(decoded_data['user_id']))
            
            # Get the user and set new password
            user = User.objects.get(id=user_id)
            user.set_password(new_password)
            user.save()

            # Clear session and cache
            del request.session['email']
            cache.delete(f'verified_otp_{email}')
            
            return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
