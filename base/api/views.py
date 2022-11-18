import email
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from .serializers import *
from .mail import *
from base.models import *
from cart.serializers import *
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password



def getTokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
 
 
class Login_user(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
            
        user = NewUserRegistration.objects.filter(email = email)
        if not user.exists():
            context = {'msg':'user with this mail does not exist'}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)
        if user is not None:
            token = getTokens(user)
            return Response({'id':user.id,'token': token,'msg':'Login Success'}, status=status.HTTP_200_OK)

        return Response({'msg':'Enter correct Password'}, status=status.HTTP_400_BAD_REQUEST)

        
class List_of_registered_user(APIView):
    def get(self, request):
        users = NewUserRegistration.objects.all()
        serializer = NewUserSerializer(users, many = True)
        return Response(serializer.data)
        
class New_user_registration(APIView): 
    def post(self, request):
            email = request.data.get("email")
            password = request.data.get("password")
            user_name = request.data.get("user_name")
            user = NewUserRegistration.objects.filter(email=email)
            if user.exists:
                return Response({'message':'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            username = NewUserRegistration.objects.filter(user_name=user_name)
            if username.exists:
                return Response({'message':'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = Verify_OTP_serializer(data=request.data)
            
            userOTP = OTP.objects.filter(email=email)
            
            if userOTP.exists() and not user.exists():
                userOTP.delete()
            
            if serializer.is_valid(raise_exception=True):            
                serializer.save()
                OTP_send = OTP.objects.get(email=serializer.data["email"])
                OTP_send.password = make_password(password)
                OTP_send.save()

                send_otp(OTP_send.email)
                
                return Response({'msg':'Please check mail for OTP'}, status=status.HTTP_200_OK)
                
        
        
    
class Profile_details(APIView):
        permission_classes = [IsAuthenticated,]
        def get(self, request):
            email = request.user.email
            user = NewUserRegistration.objects.get(email=email)
            serializer = profileSerializer(user, many=False)
            return Response(serializer.data)
    
        def put(self, request):
            email = request.user.email
            user = NewUserRegistration.objects.get(email__iexact=email)
            serializer = profileSerializer(instance=user, data = request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                Profile_serializer = profileSerializer(user, many=False)
                return Response(Profile_serializer.data, status=status.HTTP_200_OK)
            return Response({'message':'Invalid'}, status=status.HTTP_400_BAD_REQUEST)
        
        def delete(self, request):
            email = request.user.email
            user = NewUserRegistration.objects.get(email = email)
            user.delete()
            return Response({'message': 'Deleted'}, status=status.HTTP_200_OK)
    
    
class OTP_check(APIView):
    def post(self, request):
        
        serializer = otpcheckserializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data['email']
            otp = serializer.data['otp']


            userOTP = OTP.objects.get(email = email)

            if not len(userOTP.otp) == 4:
                context = {'msg':'generate new otp request'}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            if not userOTP.otp == otp:
                context = {'msg':'otp is not valid'}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            
            
            if userOTP.time_created + timedelta(minutes=2) < timezone.now():
                message = {'msg':'OTP expired'}
                return Response(message,status=status.HTTP_400_BAD_REQUEST)    
            

            NewUserRegistration.objects.create(name = userOTP.name, user_name = userOTP.user_name, email = userOTP.email, password = userOTP.password)
            user = NewUserRegistration.objects.get(email=userOTP.email)
            user.is_verified = True
            userOTP.otp = random.randint(101 , 999)
            userOTP.is_verified = True
            user.save()
            userOTP.save()
            if user is not None:
                token = getTokens(user)
                cart.objects.create(email=user.email , user = user)               
                return Response({'token': token,'msg':'verification Successfull'},status=status.HTTP_200_OK)
            
            return Response({'msg':'user does not exists'}, status=status.HTTP_400_BAD_REQUEST)

class Resend_otp(APIView):
    def post(self, request, format=None):
        serializer = resetpassserializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data['email']

            userOTP = OTP.objects.filter(email = email)
            if not userOTP.exists():
                context = {'msg':'OTP for requested user does not exists'}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            

            send_otp(serializer.data['email'])
            context = {'msg':'Check Mail for OTP'}
            return Response(context, status=status.HTTP_200_OK)



class Reset_password(APIView):
    def post(self, request):
        serializer = resetpassserializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data['email']
            user = NewUserRegistration.objects.filter(email = email)
            if not user.exists():
                context = {'msg':'user does not exist'}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
                
            send_otp(serializer.data['email'])
            context = {'msg':'check mail for otp'}
            return Response(context, status=status.HTTP_200_OK)

class New_password(APIView):
    def post(self, request):
        serializer = passchangeserializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data['email']
            otp = serializer.data['otp']
            password = serializer.data['passwordd']

            user = NewUserRegistration.objects.filter(email__iexact = email)
            userOTP = OTP.objects.get(email=email)
            if not user.exists():
                context = {'msg':'user does not exist'}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            if not len(userOTP.otp) == 4:
                context = {'msg':'generate new otp request'}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            if not userOTP.otp == otp:
                context = {'msg':'otp is not valid'}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)  
            
            chkUser = authenticate(email=email, password=password)
            
            if chkUser is not None:
                context = {'msg':'Password entered is same as old one'}
                return Response(context, status.HTTP_400_BAD_REQUEST)

            user = user.first()
            user.password = make_password(password)
            userOTP.otp = random.randint(101 , 999)
            user.save()
            userOTP.save()
            context = {'msg':'reset Successfull'}
            return Response(context, status=status.HTTP_200_OK)    
            
class Verify_check(APIView):
        permission_classes = [IsAuthenticated,]
        def get(self, request):
            email = request.user.email
            user = NewUserRegistration.objects.get(email__iexact=email)
            if user.is_verified == True:
                context = {'msg':'User is verified'}
                return Response(context, status=status.HTTP_200_OK)
                
            context = {'msg':'User is not verified'}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)