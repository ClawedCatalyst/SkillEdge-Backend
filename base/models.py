import imp

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import EmailValidator, MinValueValidator
from django.db import models
from django.utils import timezone

# from courses.models import Course


class MyUserManager(BaseUserManager):
    def create_user(self, email, name, user_name, password=None, confirm_password=None):
        """
        Creates and saves a User with the given email, name,date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name,
            user_name=user_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        name,
        user_name,
        password=None,
    ):
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


class interests(models.Model):
    interest = models.CharField(max_length=50, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.interest)


class NewUserRegistration(AbstractBaseUser):
    GENDER = (("M", "Male"), ("F", "Female"), ("O", "Others"))

    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
        validators=[EmailValidator()],
    )
    name = models.CharField(max_length=150, default=None)
    user_name = models.CharField(
        max_length=150, blank=True, null=True, default=None, unique=True
    )
    gender = models.CharField(max_length=1, choices=GENDER, blank=False, default="M")
    mobile = models.BigIntegerField(blank=True, default=91)
    picture = models.ImageField(
        upload_to="images", default="images/defaultProfilePicture_jkvski.png"
    )
    dateOfBirth = models.DateField(blank=False, default="2022-10-10")
    wallet = models.FloatField(
        validators=[MinValueValidator(0)], default=0, null=True, blank=False
    )
    # otp = models.CharField(max_length=4, blank=True, null=True)
    interested = models.ManyToManyField(interests)
    purchasedCourse = models.ManyToManyField(settings.INTEREST)
    educator_rating = models.FloatField(default=0)

    is_educator = models.BooleanField(default=False)
    is_certified_educator = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "name",
        "user_name",
    ]

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


class OTP(models.Model):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
        validators=[EmailValidator()],
        null=True,
    )
    name = models.CharField(max_length=150, default=None, null=True)
    user_name = models.CharField(
        max_length=150, blank=True, null=True, default=None, unique=True
    )
    password = models.CharField(max_length=100, null=True)
    otp = models.CharField(max_length=4, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    time_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email
