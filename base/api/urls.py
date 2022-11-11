import imp
from django.urls import path

from base.models import NewUserRegistration
from . import views
from .views import *

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('login/', Login_user.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('new_user_registration/', New_user_registration.as_view(), name='new_user_registration'),
    path('resend_otp/', Resend_otp.as_view(), name='resend_otp'),
    path('otp_verify/', OTP_check.as_view(), name='otp_verification'),
    path('reset_password/', Reset_password.as_view(), name='resetpass'),
    path('enter_new_password/', New_password.as_view(), name='newpass'),
    path('list_of_registered_users/',List_of_registered_user.as_view(), name='listOfRegisteredUser'),
    path('profile_details/',Profile_details.as_view(), name='profileDetails'),
    path('Verifycheck/',Verify_check.as_view(), name='Verifycheck')
]