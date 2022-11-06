import imp
from django.db import models
# from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from base.models import *
from courses.models import *
from django.core.validators import MaxValueValidator , MinValueValidator , EmailValidator

class cart(models.Model):
    student = models.ForeignKey(NewUserRegistration, on_delete=models.CASCADE,null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null=True)

