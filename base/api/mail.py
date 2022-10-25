from django.core.mail import send_mail
import random
from django.conf import settings
from base.models import *

def send_otp(email):
    subject = "Here's your account verification mail"
    otp = random.randint(1001 , 9999)
    otp_msg = f" your otp for account verification is {otp} "
    email_by = settings.EMAIL_HOST
    send_mail(subject , otp_msg , email_by , [email])
    user = NewUserRegistration.objects.get(email = email)
    OTP.objects.filter(verifyEmail__iexact = user).delete()
    OTP.objects.create(verifyEmail = user,time_created = timezone.now()) 
    user.otp = otp
    user.save()

