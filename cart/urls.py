from unicodedata import name
from django.urls import path
from .views import *


urlpatterns = [
    path('create_cart/', createcart.as_view(), name='createcart'),
    path('cartid/', cartid.as_view(), name='cartid'),
    path('cart/', Cart_View.as_view(), name='cart'),
]