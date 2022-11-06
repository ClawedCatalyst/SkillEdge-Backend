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
class cartadd(APIView):
    permission_classes = [IsAuthenticated,]
    def put(self,request):
        email = request.user.email
        user = NewUserRegistration.objects.get(email__iexact=email)
        ser = CartSerializer(data=request.data)
        if ser.is_valid(raise_exception=True):
            ser.save()
            ser.student = email
            ser.save()
            return Response({'msg':'course added successfully to cart'})