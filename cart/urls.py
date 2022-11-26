from unicodedata import name
from django.urls import path
from .views import *


urlpatterns = [
    path('create_cart/', Create_cart.as_view(), name='createcart'),
    path('cartid/', Cart_id.as_view(), name='cartid'),
    path('cart/', Cart.as_view(), name='cart'),
    path('cart/<str:ck>/', Cart.as_view(), name='remove_from_cart'),
    path('carttrial/', CartTrial.as_view(), name='cart'),
]