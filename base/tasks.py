from datetime import timedelta
from django.utils import timezone
from .models import *
from celery.schedules import crontab
from celery import shared_task

@shared_task(bind=True)
def delete_unwanted_email(self):
    user_otp = OTP.objects.all()
    for user in user_otp:
      if user.time_created + timedelta(minutes=5) < timezone.now() and user.is_verified == False:
          user.delete()
        
    
    return "DONE"    