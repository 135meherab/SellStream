from django.contrib import admin
from .models import EmployeeDetailsModel, ShiftModel, AttendanceModel, DesignationModel
# Register your models here.

class EmployeeDetailsAdmin(admin.ModelAdmin):
    list_display = ['id','first_name', 'last_name', 'email', 'phone', 'photo']
admin.site.register(EmployeeDetailsModel, EmployeeDetailsAdmin)

class DesignationAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'salary', 'employee']
admin.site.register(DesignationModel, DesignationAdmin)

class ShiftAdmin(admin.ModelAdmin):
    list_display = ['id','name']
admin.site.register(ShiftModel, ShiftAdmin)

class AttendanceAdmin(admin.ModelAdmin):
    list_display = [ 'id','date', 'isAttend', 'shift', 'employee']
admin.site.register(AttendanceModel, AttendanceAdmin)
