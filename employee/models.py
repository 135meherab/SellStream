from django.db import models

# Create your models here.
class EmployeeDetailsModel(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    photo = models.ImageField(upload_to='employee/media/%Y/%m/%d/', blank=True, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name
    

class ShiftModel(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class DesignationModel(models.Model):
    name = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    employee = models.ForeignKey(EmployeeDetailsModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class AttendanceModel(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    isAttend = models.BooleanField(default=False)
    shift = models.ForeignKey(ShiftModel, on_delete=models.CASCADE)
    employee = models.ForeignKey(EmployeeDetailsModel, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.employee) + str(self.date) 
