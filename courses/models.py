from django.db import models
# from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from base.models import *
from django.core.validators import MaxValueValidator , MinValueValidator , EmailValidator


# Create your models here.

class category(models.Model):
    category = models.CharField(max_length=50,null=True)
    email = models.ManyToManyField(NewUserRegistration)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.category)

class Course(models.Model):
    category = models.ForeignKey(category, on_delete=models.CASCADE,null=True)  
    topic = models.CharField(max_length=200)
    educator_mail = models.ForeignKey(NewUserRegistration, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(validators=[MaxValueValidator(999)],null=True, blank=False)
    short_description = models.CharField(max_length=200, null=True, blank=True)
    thumbnail = models.ImageField(upload_to="courses/thumbnail", height_field=None, width_field=None, max_length=100, default="")
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    review_count = models.PositiveIntegerField(null=True, default=0)
    latest_review = models.PositiveIntegerField(validators=[MaxValueValidator(5),MinValueValidator(0)],default=0)
    rating = models.FloatField(validators=[MaxValueValidator(5),MinValueValidator(0)],default=0)

    def __str__(self):
        return self.topic

class lessons(models.Model):
    
    topic = models.ForeignKey(Course, on_delete=models.CASCADE)
    description = models.TextField(max_length=2000)
    time = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.lessons[0:100]

class Feedback(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null=True)
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5),MinValueValidator(1)],default=0)
    user = models.ManyToManyField(NewUserRegistration)
    comment = models.CharField(max_length=200, null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)

    def __int__(self):
        return self.rating
