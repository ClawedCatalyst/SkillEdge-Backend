import imp

from django.contrib.auth.models import User
from django.core.validators import (EmailValidator, MaxValueValidator,
                                    MinValueValidator)
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from base.models import *
from courses.models import *


class cart(models.Model):
    user = models.OneToOneField(
        NewUserRegistration, on_delete=models.CASCADE, null=True
    )
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
        validators=[EmailValidator()],
        null=True,
    )
    total_price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.email + " [" + str(self.total_price) + "] "


class cart_courses(models.Model):
    cart = models.ForeignKey(cart, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    price = models.PositiveIntegerField(validators=[MaxValueValidator(999)], default=0)

    def __str__(self):
        return self.cart.email + " [" + self.course.topic + "] "


@receiver(pre_save, sender=cart_courses)
def addcourse(sender, **kwargs):
    cart_item = kwargs["instance"]
    course = Course.objects.get(id=cart_item.course.id)
    cart_item.price = course.price
    cart_id = cart_item.cart.id
    cart_details = cart.objects.get(id=cart_id)
    cart_totalprice = cart_details.total_price
    cart_details.total_price = course.price + cart_totalprice
    cart_details.save()
