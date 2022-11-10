import imp
from django.db import models
# from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from base.models import interests,NewUserRegistration
from django.core.validators import MaxValueValidator , MinValueValidator , EmailValidator
from django.core.validators import EmailValidator
from cloudinary_storage.storage import VideoMediaCloudinaryStorage


# Create your models here.

class Course(models.Model):
    category = models.ForeignKey(interests, on_delete=models.CASCADE,null=True)  
    topic = models.CharField(max_length=200)
    educator_mail = models.ForeignKey(NewUserRegistration, on_delete=models.CASCADE)
    educator_name = models.CharField(max_length=100, null=True)
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
    lessonName = models.TextField(max_length=200,null=True)
    file = models.FileField(upload_to="courses/video",null=True,default='', storage=VideoMediaCloudinaryStorage())
    length=models.DecimalField(max_digits=100,decimal_places=2,default=0.0)
    time = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return str(self.topic)

class feedbackmodel(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null=True)
    latest_review = models.PositiveIntegerField(validators=[MaxValueValidator(5),MinValueValidator(1)],default=0)
    user = models.CharField(max_length=200,null=True,blank=True)
    comment = models.CharField(max_length=100,default=" ")
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.course.topic + " [" + str(self.latest_review) + "] "+ self.comment[0:20]