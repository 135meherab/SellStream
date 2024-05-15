from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter() # amader router

router.register('designation', views.DesignationViews, basename="designation") 
router.register('employee', views.EmployeeViews, basename="employee") 


urlpatterns = [
    path('', include(router.urls)),

    path('attendance/', views.Attendanceview.as_view(), name="attendances"),
    path('attendance/<int:pk>', views.AttendanceviewRetrive.as_view(), name="attendance"),
    
    path('leave/', views.Leaveview.as_view(), name="leave"),
]