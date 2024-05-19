from django.contrib import admin
from .models import DesignationModel, EmployeeModel, AttendanceModel, LeaveModel, SpecialOccasionModel
# Register your models here.


admin.site.register(DesignationModel)

admin.site.register(EmployeeModel)

admin.site.register(AttendanceModel)

admin.site.register(LeaveModel)

admin.site.register(SpecialOccasionModel)