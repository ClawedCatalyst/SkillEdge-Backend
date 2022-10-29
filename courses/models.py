from django.db import models
# from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from base.models import *

# Create your models here.

class category(models.Model):
    category = models.CharField(max_length=50,null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category

class Course(models.Model):
    category = models.ForeignKey(category, on_delete=models.CASCADE,null=True)
    topic = models.CharField(max_length=200)
    educator_mail = models.ForeignKey(NewUserRegistration, on_delete=models.CASCADE)
    short_description = models.CharField(max_length=200, null=True, blank=True)
    thumbnail = models.ImageField(upload_to="thumbnail", height_field=None, width_field=None, max_length=100, default="")
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.topic

class lessons(models.Model):
    
    topic = models.ForeignKey(Course, on_delete=models.CASCADE)
    description = models.TextField(max_length=2000)
    time = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.lessons[0:100]