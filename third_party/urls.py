from django.urls import path
from .views import UserProfileView

urlpatterns = [
    path('firebase/', UserProfileView.as_view(), name='user-profile'),
]

# from django.urls import path
# from .views import GoogleLoginView

# urlpatterns = [
#     path('google/', GoogleLoginView.as_view(), name='google-login'),
# ]