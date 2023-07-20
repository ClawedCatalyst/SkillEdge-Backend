import random

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail


def send_course_confirmation(email):
    subject = "You're in! Order Confirmation"
    text = f"Thanks For buying The Course(s) !!\n We wish you a great and joyable learning !!"
    style = f'<p><strong style="font-size: 18px;">Thanks For buying The Course(s) !!</strong></p><p style="font-size: 18px;">We wish you a great and joyable learning !!</p><div style="text-align:center; font-size:40px; color:grey; margin-top:20px;"><strong>SKILL EDGE</strong></div>'
    email_by = settings.EMAIL_HOST
    course_confirmation_msg = EmailMultiAlternatives(subject, text, email_by, [email])
    course_confirmation_msg.attach_alternative(style, "text/html")
    course_confirmation_msg.send()
