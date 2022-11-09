from unicodedata import name
from django.urls import path
from .views import *


urlpatterns = [
    path('buy_courses/', BuyCourseView.as_view(), name='addCourse'),
]
