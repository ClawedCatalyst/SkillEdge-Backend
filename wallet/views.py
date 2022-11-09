from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from courses.models import *
from base.models import *
from cart.models import *
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class BuyCourseView(APIView):
    permission_classes = [IsAuthenticated,]
    def put(self,request):
        email = request.user.email
        student = NewUserRegistration.objects.get(email__iexact=email)
        cart_details = cart.objects.get(email__iexact =email)
        cart_id = cart_details.id
        totalprice=cart_details.total_price
        stu_balance = student.wallet
        if stu_balance < totalprice :
            amount = totalprice - stu_balance
            return Response({'message':'Low Balance!' , 'Amount to be added to buy this course' : amount })
        stu_new_balance = stu_balance - totalprice
        student.wallet = stu_new_balance
        courses= cart_courses.objects.filter(cart=cart_id)
        # print(courses)
        ser = WalletSerializer(instance=student, data = request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response({'message':'transaction failed'})
        