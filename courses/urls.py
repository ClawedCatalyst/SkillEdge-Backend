from unicodedata import name
from django.urls import path
from .views import *


urlpatterns = [
    path('course/', CourseView.as_view(), name='addCourse'),
    path('category/', CategoryView.as_view(), name='AddCategory'),
    path('view_filtered_courses/', ViewFilteredCourses.as_view(), name='viewFilteredCourses'),
    path('rate_course/', CourseRating.as_view(), name='rateCourse'),
    path('course_feedback/<str:ck>/', CourseFeedback.as_view(), name='course_feedback'),
    path('search_course/', Searching.as_view(), name='searchCourse'),
    path('lesson/', LessonView.as_view(), name='LessonView'),
    path('purchased_courses/', Purchasedcourses.as_view(), name='purchased_courses'),
    path('view_specific_lesson/', ViewSpecificCourseLesson.as_view(), name='viewSpecificCourseLesson')
]