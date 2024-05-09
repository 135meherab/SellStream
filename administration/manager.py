from django.contrib.auth.models import BaseUserManager

#  Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, fullname, phone, bio, password=None, password2=None):
        """
        Creates and saves a User with the given email, email, fullname, bio and password.
        """
        if not email:
            raise ValueError('User must have an email')

        user = self.model(
            email = self.normalize_email(email),
            fullname = fullname,
            phone = phone,
            bio = bio,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fullname, phone, bio, password=None):
        """
        Creates and saves a superuser with the given username, email, fullname, bio and password.
        """
        user = self.create_user(
            email = email,
            password = password,
            fullname = fullname,
            phone=phone,
            bio = bio,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user