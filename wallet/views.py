from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from courses.models import *
from base.models import *

# Create your views here.
class BuyCourseView(APIView):
    def put(self,request,ck,sk):
        crs = Course.objects.get(id = ck)
        student = NewUserRegistration.objects.get(id = sk)
        edu = GetEducatorSerializer(crs)
        price = crs.price
        income = 0.85 * price
        edu_mail = crs.educator_mail
        educator = NewUserRegistration.objects.get(email = edu_mail)
        stu_balance = student.wallet
        edu_balance = educator.wallet
        new_balance = edu_balance + income
        if stu_balance < income :
            amount = income - stu_balance
            return Response({'message':'low balance. add' , 'amount to be added to buy this course' : amount })
        stu_new_balance = stu_balance - income
        educator.wallet = new_balance
        student.wallet = stu_new_balance
        # student = NewUserRegistration.objects.get(id=sk)
        # return Response(new_balance)
        serializer = WalletSerializer(instance=educator, data = request.data)
        if serializer.is_valid():
            serializer.save()
        ser = WalletSerializer(instance=student, data = request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response({'message':'transaction failed'})
        