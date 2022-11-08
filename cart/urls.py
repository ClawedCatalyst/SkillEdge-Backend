from unicodedata import name
from django.urls import path
from .views import *


urlpatterns = [
    path('create_cart/', createcart.as_view(), name='add_to_cart'),
    path('cartid/', cartid.as_view(), name='cartid'),
    path('add_to_cart/', cartadd.as_view(), name='add_to_cart'),
    path('remove_from_cart/<str:ck>/', cartremove.as_view(), name='remove_from_cart'),
]