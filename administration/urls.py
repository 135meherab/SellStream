from django.urls import path
from .views import AdminLoginApiview, AdminLogoutAPIView, ProfileView, ChangePasswordView

urlpatterns = [
    path('login/', AdminLoginApiview.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', AdminLogoutAPIView.as_view(), name='logout'),
    path('change_password/', ChangePasswordView.as_view(), name='change-password'),
]