from unicodedata import name
from django.urls import path
from .views import *


urlpatterns = [
    path('add_course/<str:pk>/', CourseView.as_view(), name='addCourse'),
    path('rate_course/<str:ck>/', CourseRating.as_view(), name='rateCourse'),
    path('view_course/', ViewAllCourses.as_view(), name='viewCourse'),
]

