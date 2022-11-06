from unicodedata import name
from django.urls import path
from .views import *


urlpatterns = [
    path('add_to_cart/', cartadd.as_view(), name='add_to_cart'),
]