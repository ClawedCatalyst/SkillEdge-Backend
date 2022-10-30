from django.urls import path
from .views import *

urlpatterns = [
    path('become_educator/<str:pk>',BecomeEducator.as_view(),name='becomeEducator'),
]
