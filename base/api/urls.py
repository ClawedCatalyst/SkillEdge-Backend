import imp
from django.urls import path

from base.models import NewUserRegistration
from . import views
from .views import *

from rest_framework_simplejwt.views import (
    # TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('new_user_registration/', NewUserRegistrationView.as_view(), name='new_user_registration'),
    path('otp_verify/', otp_check.as_view(), name='otp_verification'),
]
