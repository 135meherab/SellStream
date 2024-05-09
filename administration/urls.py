from django.urls import path
from .views import AdminLoginApiview, AdminLogoutAPIView, ProfileView

urlpatterns = [
    path('login/', AdminLoginApiview.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', AdminLogoutAPIView.as_view(), name='logout'),
]