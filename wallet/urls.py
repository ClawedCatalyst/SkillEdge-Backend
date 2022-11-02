from unicodedata import name
from django.urls import path
from .views import *


urlpatterns = [
    path('buy_course/<str:ck>/<str:sk>/', BuyCourseView.as_view(), name='addCourse'),
]
