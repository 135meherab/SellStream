from django.db import models
from shop.models import Shop, Branch
# Create your models here.
class DesignationModel(models.Model):
    owner = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    


GENDER = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]
class EmployeeModel(models.Model):
    designation = models.ForeignKey(DesignationModel, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    bank_account = models.CharField(max_length=30, unique=True)
    gender = models.CharField(max_length=30, choices=GENDER, default='Male')
    is_manager = models.BooleanField(default=False)

    def __str__(self):
        return self.fullname
    
    

SHIFT = [
    ('Morning', 'Morning'),
    ('Evening', 'Evening'),
]
class AttendanceModel(models.Model):
    employee = models.ForeignKey(EmployeeModel, on_delete=models.CASCADE)
    is_attend = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    shift = models.CharField(max_length=30, choices=SHIFT, default='Morning')

    def __str__(self):
        return str(self.employee)

class LeaveModel(models.Model):
    employee = models.ForeignKey(EmployeeModel, on_delete=models.CASCADE)
    start_leave = models.DateField()
    end_leave = models.DateField()
    total_day = models.IntegerField()
    description = models.TextField()
    
    def __str__(self):
        return str(self.employee)