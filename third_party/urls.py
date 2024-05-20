from django.urls import path
from .views import UserProfileView

urlpatterns = [
    path('firebase/', UserProfileView.as_view(), name='user-profile'),
]