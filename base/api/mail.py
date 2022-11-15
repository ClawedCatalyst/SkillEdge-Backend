from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
import random
from django.conf import settings
from base.models import *
from django.utils import timezone

def send_otp(email):
    subject = "Here's your account verification mail"
    otp = random.randint(1001 , 9999)
    text  = f'Your One Time Password for verification on Skill-Edge is {otp}.\nValid for only 2 minutes.\n DO NOT SHARE IT WITH ANYBODY.\nSKILL EDGE'
    style = f'<p>Your One Time Password for verification on Skill-Edge is <strong style="font-size: 18px;">{otp}</strong>.</p><p>Valid for only 2 minutes.</p><p style="font-size: 18px;">DO NOT SHARE IT WITH ANYBODY.</p><div style="text-align:center; font-size:40px; color:grey; margin-top:20px;"><strong>SKILL EDGE</strong></div>'
    email_by = settings.EMAIL_HOST
    otp_msg = EmailMultiAlternatives(subject, text,email_by,[email])
    otp_msg.attach_alternative(style, "text/html")
    otp_msg.send()
    user = NewUserRegistration.objects.get(email = email)
    OTP.objects.filter(verifyEmail__iexact = user.email).delete()
    OTP.objects.create(verifyEmail = user,time_created = timezone.now()) 
    user.otp = otp
    user.save()
    # comparision_time = timezone.now() - timedelta(minutes=3)
    # otp_record = OTP.objects.filter(time_created__gte = comparision_time)
    # for each_record in otp_record
    #     each_record.delete()

