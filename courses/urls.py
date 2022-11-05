from unicodedata import name
from django.urls import path
from .views import *


urlpatterns = [
    path('add_course/', CourseView.as_view(), name='addCourse'),
    path('view_course/', ViewAllCourses.as_view(), name='viewCourse'),
    path('view_category/', ViewAllCategories.as_view(), name='viewCategory'),
    path('add_category/', AddCategoryUser.as_view(), name='AddCategory'),
    path('rate_course/', CourseRating.as_view(), name='rateCourse'),
]

