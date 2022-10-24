from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class MyUserManager(BaseUserManager):
    def create_user(self, email, name, user_name, password=None, confirm_password=None):
        """
        Creates and saves a User with the given email, name,date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            user_name=user_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, user_name, password=None,):
        """
        Creates and saves a superuser with the given email,name, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            user_name=user_name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user



class NewUserRegistration(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address',
        max_length=255,
        unique=True,)
    name = models.CharField(max_length=150, default=None)
    user_name = models.CharField(max_length=150, blank=True, null=True, default='none')

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','user_name',]
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
