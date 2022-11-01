from unicodedata import name
from django.urls import path
from .views import *


urlpatterns = [
    path('add_course/<str:pk>/', CourseView.as_view(), name='addCourse'),
    path('view_course/', ViewAllCourses.as_view(), name='viewCourse')
]