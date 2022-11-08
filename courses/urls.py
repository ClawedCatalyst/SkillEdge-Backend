from unicodedata import name
from django.urls import path
from .views import *


urlpatterns = [
    path('add_course/', CourseView.as_view(), name='addCourse'),
    path('view_course/', ViewAllCourses.as_view(), name='viewCourse'),
    path('view_category/', ViewAllCategories.as_view(), name='viewCategory'),
    path('add_category/', AddCategoryUser.as_view(), name='AddCategory'),
    path('view_filtered_courses/', viewFilteredCourses.as_view(), name='viewFilteredCourses'),
    path('rate_course/', CourseRating.as_view(), name='rateCourse'),
    path('search_course/', searching.as_view(), name='searchCourse'),
    path('lesson/', LessonView.as_view(), name='LessonView'),
    path('view_specific_lesson/', viewSpecificCourseLesson.as_view(), name='viewSpecificCourseLesson')
]

