from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework.authtoken.views import obtain_auth_token

#router = DefaultRouter()
#router.register('ratings', views.RatingGetPost,basename="rate")
urlpatterns = [
    path('',views.RatingGetPost.as_view(),name='rating_get_post'),
    path('<int:pk>/',views.RatingUpdate.as_view(),name='rating_update'),
]