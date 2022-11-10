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
    def put(self,request,ck):
        email = request.user.email
        student = NewUserRegistration.objects.get(email__iexact=email)
        crs = Course.objects.get(id = ck)
        edu = GetEducatorSerializer(crs)
        price = crs.price
        income = 0.85 * price
        edu_mail = crs.educator_mail
        educator = NewUserRegistration.objects.get(email = edu_mail)
        stu_balance = student.wallet
        edu_balance = educator.wallet
        new_balance = edu_balance + income
        array = student.purchasedCourse.all()
        for a in array:
            if (a.id==int(ck)) :
                return Response({'msg':'course already purchased'})
        if stu_balance < price :
            amount = price - stu_balance
            return Response({'message':'low balance. add' , 'amount to be added to buy this course' : amount })
        stu_new_balance = stu_balance - price
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
            cart_details = cart.objects.get(email__iexact =email)
            cart_id = cart_details.id
            totalprice = cart_details.total_price
            c_status = cart_courses.objects.filter(cart = cart_id, course = ck)
            if len(c_status) != 0:
                c_status.delete()
                cart_details.total_price = totalprice - price
                cart_details.save()
            student.purchasedCourse.add(crs.id)
            student.save()
            return Response(ser.data)
        return Response({'message':'transaction failed'})

class BuyAllCourseView(APIView):
    permission_classes = [IsAuthenticated,]
    def put(self,request):
        email = request.user.email
        student = NewUserRegistration.objects.get(email__iexact=email)
        if student.is_verified == False:
            return Response({'message':'You are not verified! Verify your mail'})
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
        for crs_id in courses:
            crs = Course.objects.get(id=crs_id.course.id)
            # edu = GetEducatorSerializer(crs)
            price = crs.price
            income = 0.85 * price
            edu_mail = crs.educator_mail
            educator = NewUserRegistration.objects.get(email = edu_mail)
            edu_balance = educator.wallet
            new_balance = edu_balance + income
            educator.wallet = new_balance
            student.purchasedCourse.add(crs.id)
            student.save()
            serializer = WalletSerializer(instance=educator, data = request.data)
            if serializer.is_valid():
                serializer.save()
                crs_id.delete()  
        # print(cart_details)
        cart_details.total_price=0
        cart_details.save()
        ser = WalletSerializer(instance=student, data = request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response({'message':'transaction failed'})
        