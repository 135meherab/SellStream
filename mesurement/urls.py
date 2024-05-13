from django.urls import path, include
from rest_framework.routers import DefaultRouter

# from .views import Product, Order_create,Order_list,Customer_create,Customer_list,CustomerDelete,Uom_create,Uom_list,Category_create,Category_list
from . import views

router = DefaultRouter()
router.register('create',views.CreateMesurement)
urlpatterns = [
    path('', include(router.urls)), 
    path('list/', views.MesurementList.as_view()),
]
