from unicodedata import name

from django.urls import path

from .views import *

urlpatterns = [
    path("buy_course/<int:ck>/", BuyCourseView.as_view(), name="BuyCourse"),
    path("buy_allcourses/", BuyAllCourseView.as_view(), name="BuyAllCourse"),
]
