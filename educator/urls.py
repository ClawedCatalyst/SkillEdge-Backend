import imp
from django.urls import path

from .models import NewUserRegistration
from .views import *


urlpatterns = [
    path('login/', loginUser.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('new_user_registration/', NewUserRegistrationView.as_view(), name='new_user_registration'),
    path('resend_otp/', resend_otp.as_view(), name='resend_otp'),
    path('otp_verify/', otp_check.as_view(), name='otp_verification'),
    path('reset_password/', resetpassView.as_view(), name='resetpass'),
    path('enter_new_password/', newpassView.as_view(), name='newpass'),
    path('list_of_registered_users/',listOfRegisteredUser.as_view(), name='listOfRegisteredUser'),
    path('profile_details/<str:pk>',profileDetails.as_view(), name='profileDetails')
]