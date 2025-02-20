from django.urls import path, include
from .views import (
    RegisterAPIView,
    EmailVerificationView,
    UserLogin,
    UserLogout,
    UserDetailView,
    UserUpdateView,
    PasswordChangeView,
    ShopCreateView,
    ShopList,
    ShopUpdateView,
    Branchviewset,
    PasswordResetView,
    VerifyOTPView,
    PasswordChangeViews
)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('branch',Branchviewset)
urlpatterns = [
    path('', include(router.urls)),
    path('sign_up/', RegisterAPIView.as_view(), name='sign_up'),
    path('activate/<uid64>/<token>/', EmailVerificationView.as_view(), name='email-verification'),
    path('login/', UserLogin.as_view(), name='Login'),
    path('logout/', UserLogout.as_view(), name='Logout'),
    path('user_details/', UserDetailView.as_view(), name='user-detail'),
    path('user/update/', UserUpdateView.as_view(), name='user-update'),
    path('user/password/change/', PasswordChangeView.as_view(), name='password-change'),
    path('createshop/', ShopCreateView.as_view(), name='shop-create'),
    path('get/', ShopList.as_view(), name='shop-list'),
    path('update/', ShopUpdateView.as_view(), name='shop-update'),
    path('password/reset/request/', PasswordResetView.as_view(), name='password-reset-request'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('password-change/', PasswordChangeViews.as_view(), name='password_change_url'),
]