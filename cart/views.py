from django.shortcuts import render
from rest_framework import status
from logging import raiseExceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *
from base.models import *

# Create your views here.
class createcart(APIView):
    def post(self,request):
        ser = CartSerializer(data=request.data)
        if ser.is_valid(raise_exception=True):
            ser.save()
            return Response({'msg':'cart added successfully'})

class cartid(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self,request):
        email = request.user.email
        cart_details = cart.objects.get(student_mail__iexact =email)
        cart_id = cart_details.id
        return Response(cart_id)

class cartadd(APIView):
    permission_classes = [IsAuthenticated,]
    def put(self,request):
        email = request.user.email
        user = NewUserRegistration.objects.get(email__iexact=email)
        ser = AddCartSerializer(data=request.data)
        if ser.is_valid(raise_exception=True):
            ser.save()
            return Response({'msg':'course added successfully to cart'})

class cartremove(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self,request,ck):
        email = request.user.email
        user = NewUserRegistration.objects.get(email__iexact=email)
        ct = cart.objects.get(student_mail__iexact =email)
        # print(ct.id)
        cart_courseid = cart_courses.objects.get(cart=ct.id,course=ck)
        cart_courseid.delete()
        return Response({'msg':'course removed successfully from cart'})