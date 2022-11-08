import django_filters

from courses.models import *

class CartCourseFilter(django_filters.FilterSet):
    class Meta:
        model = Course
        fields = ['id']