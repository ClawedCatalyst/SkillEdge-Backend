from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.utils import timezone
from .serializers import *
from .mail import *
from base.models import *
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password

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
    
class listOfRegisteredUser(APIView):
     def get(self, request, format = None):
        users = NewUserRegistration.objects.all()
        serializer = NewUserSerializer(users, many = True)
        Serializer_list = [serializer.data]

        return Response(Serializer_list)



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
            
            email = ser.data['email']
            query  = OTP.objects.filter(verifyEmail = email)
            if not query.exists():
                context = {'msg':'please raise otp first'}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            
            userOTP = OTP.objects.get(verifyEmail__iexact = email)
            
            
            user = NewUserRegistration.objects.filter(email = email)
            if not user.exists():
                context = {'msg':'user does not exist'}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            if not len(user[0].otp) == 4:
                context = {'msg':'generate new otp request'}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            if not user[0].otp == otp:
                context = {'msg':'otp is not valid'}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            
            if userOTP.time_created + timedelta(minutes=2) < timezone.now():
                message = {'message':'OTP expired'}
                return Response(message,status=status.HTTP_400_BAD_REQUEST)    
            


            user = user.first()
            user.is_verified = True
            user.otp = random.randint(101 , 999)
            user.save()
            

            context = {'msg':'verification Successfull'}
            return Response(context, status=status.HTTP_200_OK)

class resetpassView(APIView):
    def post(self, request):
        ser = resetpassserializer(data=request.data)
        if ser.is_valid(raise_exception=True):
            email = ser.data['email']
            user = NewUserRegistration.objects.filter(email = email)
            if not user.exists():
                context = {'msg':'user does not exist'}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
                
            send_otp(ser.data['email'])
            context = {'msg':'check mail for otp'}
            return Response(context, status=status.HTTP_200_OK)

class newpassView(APIView):
    def post(self, request):
        ser = passchangeserializer(data=request.data)
        if ser.is_valid(raise_exception=True):
            email = ser.data['email']
            otp = ser.data['otp']
            pas = ser.data['passwordd']
            con_pas =ser.data['confirm_passwordd']

            user = NewUserRegistration.objects.filter(email = email)
            if not user.exists():
                context = {'msg':'user does not exist'}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            if not len(user[0].otp) == 4:
                context = {'msg':'generate new otp request'}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            if not user[0].otp == otp:
                context = {'msg':'otp is not valid'}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)   

            if pas == con_pas:
                user = user.first()
                user.password = make_password(pas)
                user.is_verified = True
                user.otp = random.randint(101 , 999)
                user.save()
            

            context = {'msg':'reset Successfull'}
            return Response(context, status=status.HTTP_200_OK)