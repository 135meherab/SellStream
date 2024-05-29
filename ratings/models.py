from django.db import models
from django.contrib.auth.models import User
# Create your models here.
star_choice = [
    (1,1),
    (2,2),
    (3,3),
    (4,4),
    (5,5),
]
class Ratings(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.SET_NULL)
    rate = models.CharField(max_length=10,choices=star_choice)
    comment = models.TextField(max_length=200,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return f'{self.user} - {self.rate}'