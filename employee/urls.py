from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViews, DesignationViews, ShiftViews, AttendanceViews, EmployeeView, AttendanceView

router = DefaultRouter()


router.register(r'designation', DesignationViews)



urlpatterns = [
    path('', include(router.urls)),

    path('shift/', ShiftViews.as_view(), name="shift"),

    path('attendance/', AttendanceViews.as_view({'get': 'list', 'post': 'create'}), name="attendance"),
    path('attendance/<int:pk>/', AttendanceView.as_view({'put': 'update'}), name="attendance"),
    
    path('employees/', EmployeeViews.as_view({'get': 'list', 'post': 'create'}), name='employee-list'),
    path('employees/<int:pk>/', EmployeeView.as_view({'get': 'retrieve', 'delete': 'destroy'}), name='employee-detail'),
]