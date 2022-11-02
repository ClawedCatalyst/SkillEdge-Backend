from django.urls import path
from .views import *

urlpatterns = [
    path('become_educator/',BecomeEducator.as_view(),name='becomeEducator'),
]
