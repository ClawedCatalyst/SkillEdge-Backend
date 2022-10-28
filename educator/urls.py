import imp
from django.urls import path

from base.models import NewUserRegistration
from . import views
from .views import *

urlpatterns = [
    path('become_educator/<str:pk>',BecomeEducator.as_view(),name='becomeEducator')
]
