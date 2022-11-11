from django.urls import path

from .views import *

urlpatterns = [
    # path('pay/', startPayment.as_view(), name="payment"),
    # path('payment_success/', handle_payment_success.as_view(), name="payment_success"),
    path('flutter_razorpay/', Flutter_Razorpay.as_view(), name="flutter_razorpay")
]
