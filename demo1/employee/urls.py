from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViews, DesignationViews, ShiftViews, AttendanceViews

router = DefaultRouter()
router.register(r'employee', EmployeeViews)
router.register(r'shift', ShiftViews)
router.register(r'designation', DesignationViews)
router.register(r'attendance', AttendanceViews)


urlpatterns = [
    path('', include(router.urls)),
]