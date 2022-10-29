from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from courses.models import *
from base.models import *

# Create your views here.
class BuyCourseView(APIView):
    def put(self,request,ck):
        crs = Course.objects.get(id = ck)
        edu = GetEducatorSerializer(crs)
        price = crs.price
        income = 0.85 * price
        edu_mail = crs.educator_mail
        educator = NewUserRegistration.objects.get(email = edu_mail)
        balance = educator.wallet
        new_balance = balance + income
        educator.wallet = new_balance
        # student = NewUserRegistration.objects.get(id=sk)
        # return Response(new_balance)
        serializer = WalletSerializer(instance=educator, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message':'transaction failed'}, status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request, ck):
        