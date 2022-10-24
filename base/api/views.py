from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import *
from .mail import *
from base.models import *

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['user_name'] = user.user_name
        return (token)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    


class NewUserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = NewUserSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            send_otp(serializer.data['email'])
            context = {'msg':'Registration Successfull'}
            return Response(context, status=status.HTTP_200_OK)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

class otp_check(APIView):
    def post(self, request):
        ser = otpcheckserializer(data=request.data)

        if ser.is_valid(raise_exception=True):
            email = ser.data['email']
            otp = ser.data['otp']

            user = NewUserRegistration.objects.filter(email = email)
            if not user.exists():
                context = {'msg':'user does not exist'}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            if not user[0].otp == otp:
                context = {'msg':'otp is not valid'}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            user = user.first()
            user.is_verified = True
            user.save()
            

            context = {'msg':'verification Successfull'}
            return Response(context, status=status.HTTP_200_OK)

        
