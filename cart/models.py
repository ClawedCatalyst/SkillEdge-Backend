import imp
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from base.models import *
from courses.models import *
from django.core.validators import MaxValueValidator , MinValueValidator , EmailValidator
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver

class cart(models.Model):
    student = models.ForeignKey(NewUserRegistration, on_delete=models.CASCADE,null=True)
    total_price = models.PositiveIntegerField(default=0)

class cart_courses(models.Model):
    cart = models.ForeignKey(cart, on_delete=models.CASCADE,null=True)
    student = models.ForeignKey(NewUserRegistration, on_delete=models.CASCADE,null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null=True)
    price = models.PositiveIntegerField(validators=[MaxValueValidator(999)],null=True, blank=False)

@receiver(post_save, sender = cart_courses)
def addcourse(sender, **kwargs):
    cart_item = kwargs['instance']
    course = Course.objects.get(id=cart_item.course.id)
    cart_courses.price = course.price
    