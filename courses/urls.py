from unicodedata import name
from django.urls import path
from .views import *


urlpatterns = [
    path('course/', Course_view.as_view(), name='addCourse'),
    path('category/', Category_view.as_view(), name='AddCategory'),
    path('view_filtered_courses/', View_filtered_courses.as_view(), name='viewFilteredCourses'),
    path('rate_course/', Course_rating.as_view(), name='rateCourse'),
    path('course_feedback/<str:ck>/', Course_feedback.as_view(), name='course_feedback'),
    path('search_course/', Searching.as_view(), name='searchCourse'),
    path('lesson/', Lesson_view.as_view(), name='LessonView'),
    path('purchased_courses/', Purchased_courses.as_view(), name='purchased_courses'),
    path('view_specific_lesson/', View_specific_course_lesson.as_view(), name='viewSpecificCourseLesson')
]