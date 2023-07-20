from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from base.models import *

from .models import Order
from .serializers import *
from .serializers import OrderSerializer


class Flutter_Razorpay(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        email = request.user.email
        user = NewUserRegistration.objects.get(email=email)
        transaction_history = Order.objects.filter(user_mail=user.id)
        serializer = OrderSerializer(transaction_history, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            email = request.user.email
            user = NewUserRegistration.objects.get(email=email)
            request.POST._mutable = True
            request.data["user_mail"] = request.user.id
            request.POST._mutable = False
            serializer = OrderSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                user.wallet += int(serializer.data["order_amount"])
                if user.wallet < 0:
                    return Response(
                        {"msg": "Not enough Balance"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                user.save()
                return Response(serializer.data)
        except:
            return Response(
                {"msg": "Payment Failed"}, status=status.HTTP_400_BAD_REQUEST
            )
