from django.shortcuts import render
from rest_framework import status
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
        if student.is_verified == False:
            return Response({'msg':'You are not verified! Verify your mail'}, status=status.HTTP_400_BAD_REQUEST)
        course = Course.objects.get(id = ck)
        educator_details = GetEducatorSerializer(course)
        price = course.price
        income = 0.85 * price
        educator_details_mail = course.educator_mail
        educator = NewUserRegistration.objects.get(email = educator_details_mail)
        student_balance = student.wallet
        educator_details_balance = educator.wallet
        new_balance = educator_details_balance + income
        purchased_courses = student.purchasedCourse.all()
        for purchased_course in purchased_courses:
            if (purchased_course.id==int(ck)) :
                return Response({'msg':'course already purchased'}, status=status.HTTP_400_BAD_REQUEST)
        if student_balance < price :
            amount = price - student_balance
            return Response({'msg':'low balance. add' , 'amount to be added to buy this course' : amount }, status=status.HTTP_400_BAD_REQUEST)
        student_new_balance = student_balance - price
        educator.wallet = new_balance
        student.wallet = student_new_balance
        serializer_eduactor = WalletSerializer(instance=educator, data = request.data)
        if serializer_eduactor.is_valid():
            serializer_eduactor.save()
        serializer_student = WalletSerializer(instance=student, data = request.data)
        if serializer_student.is_valid():
            serializer_student.save()
            cart_details = cart.objects.get(email__iexact =email)
            cart_id = cart_details.id
            totalprice = cart_details.total_price
            cart_status = cart_courses.objects.filter(cart = cart_id, course = ck)
            if len(cart_status) != 0:
                cart_status.delete()
                cart_details.total_price = totalprice - price
                cart_details.save()
            student.purchasedCourse.add(course.id)
            student.save()
            return Response(serializer_student.data)
        return Response({'msg':'transaction failed'}, status=status.HTTP_400_BAD_REQUEST)

class BuyAllCourseView(APIView):
    permission_classes = [IsAuthenticated,]
    def put(self,request):
        email = request.user.email
        student = NewUserRegistration.objects.get(email__iexact=email)
        if student.is_verified == False:
            return Response({'msg':'You are not verified! Verify your mail'}, status=status.HTTP_400_BAD_REQUEST)
        cart_details = cart.objects.get(email__iexact =email)
        cart_id = cart_details.id
        totalprice=cart_details.total_price
        student_balance = student.wallet
        if student_balance < totalprice :
            amount = totalprice - student_balance
            return Response({'msg':'Low Balance!' , 'Amount to be added to buy this course' : amount }, status=status.HTTP_400_BAD_REQUEST)
        student_new_balance = student_balance - totalprice
        student.wallet = student_new_balance
        courses= cart_courses.objects.filter(cart=cart_id)
        if len(courses)==0:
            return Response({'msg':'no courses in cart'}, status=status.HTTP_400_BAD_REQUEST)
        # print(courses)
        for course_id in courses:
            course = Course.objects.get(id=course_id.course.id)
            # edu = GetEducatorSerializer(course)
            price = course.price
            income = 0.85 * price
            educator_details_mail = course.educator_mail
            educator = NewUserRegistration.objects.get(email = educator_details_mail)
            educator_details_balance = educator.wallet
            new_balance = educator_details_balance + income
            educator.wallet = new_balance
            student.purchasedCourse.add(course.id)
            student.save()
            serializer_eduactor = WalletSerializer(instance=educator, data = request.data)
            if serializer_eduactor.is_valid():
                serializer_eduactor.save()
                course_id.delete()  
        # print(cart_details)
        cart_details.total_price=0
        cart_details.save()
        serializer_student = WalletSerializer(instance=student, data = request.data)
        if serializer_student.is_valid():
            serializer_student.save()
            return Response(serializer_student.data)
        return Response({'msg':'transaction failed'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        email = request.user.email
        student = NewUserRegistration.objects.get(email__iexact=email)
        return Response(student.wallet)
        