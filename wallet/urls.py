from unicodedata import name
from django.urls import path
from .views import *


urlpatterns = [
    path('buy_course/', BuyCourseView.as_view(), name='addCourse'),
]
