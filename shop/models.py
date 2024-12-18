from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now, timedelta

# Create your models here.
class Shop(models.Model):
      user = models.OneToOneField(User, on_delete=models.CASCADE)
      name = models.CharField(max_length=100)
      address = models.TextField()
      phone = models.CharField(max_length=20)
      
      
      def __str__(self):
            return self.name
      
class Branch(models.Model):
      shop = models.ForeignKey(Shop,related_name='branches', on_delete=models.CASCADE)
      user = models.OneToOneField(User, on_delete=models.CASCADE)
      name = models.CharField(max_length=50)
      location = models.TextField()

      
      def __str__(self):
            return self.name
      

class OTP(models.Model):
    user_email = models.EmailField(unique=True)
    otp_encrypted = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    failed_attempts = models.PositiveIntegerField(default=0)
    is_verified = models.BooleanField(default=False)

    def is_valid(self):
        """Check if the OTP is still valid."""
        return now() < self.expires_at

    def save(self, *args, **kwargs):
        # If the OTP is being created, set expiration time to 1 minute after creation
        if not self.pk:  # This is when the OTP is being created (not updated)
            self.expires_at = now() + timedelta(minutes=1)
        elif self.is_verified:  # After OTP is verified, set expiration time to 3 minutes after verification
            self.expires_at = now() + timedelta(minutes=3)

        # Automatically delete expired OTPs before saving a new one
        self.delete_expired_otps()

        super().save(*args, **kwargs)

    @classmethod
    def delete_expired_otps(cls):
        """Delete expired OTPs automatically on every query."""
        cls.objects.filter(expires_at__lt=now()).delete()