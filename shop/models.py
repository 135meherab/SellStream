from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Shop(models.Model):
      user = models.OneToOneField(User, on_delete=models.CASCADE)
      name = models.CharField(max_length=100)
      address = models.TextField()
      phone = models.CharField(max_length=20)
      
      
      def __str__(self):
            return self.name
      
class Branch(models.Model):
      shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
      user = models.OneToOneField(User, on_delete=models.CASCADE)
      name = models.CharField(max_length=50)
      location = models.TextField()

      
      def __str__(self):
            return self.name
      