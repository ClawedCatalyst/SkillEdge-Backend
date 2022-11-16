from dataclasses import field
from base.models import OTP, NewUserRegistration
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
import re
from django.core.exceptions import ValidationError

class NewUserSerializer(ModelSerializer):
    class Meta:
        model = NewUserRegistration
        fields = ["id","name","user_name", "email", "password", "is_verified","is_educator","wallet"]
        extra_kwargs={
            'password':{'write_only': True},
        }
    
    def create(self, validate_data):
        return NewUserRegistration.objects.create_user(**validate_data)
    

class loginSerializer(ModelSerializer):
    class Meta:
        model = NewUserRegistration
        fields = ["email","password"]


class profileSerializer(ModelSerializer):
    class Meta:
        model = NewUserRegistration
        fields = ("name", "user_name" ,"picture", "gender","dateOfBirth","mobile","is_educator","email","is_certified_educator","educator_rating")
        
        extra_kwargs = {'email': {'required': False ,"allow_null": True},}
    

class otpcheckserializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

class resetpassserializer(serializers.Serializer):
    email = serializers.EmailField()

class passchangeserializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    passwordd = serializers.CharField(required=True)
    
    def validate_password(self, data):
            if len(data) < 8 :
                raise ValidationError(
                    ("The password needs to be more than 8 characters")
                )
            
            if not re.findall('\d', data):
                raise ValidationError(
                    ("The password must contain at least 1 digit, 0-9."),
                    code='password_no_number',
                )
            if not re.findall('[A-Z]', data):
                raise ValidationError(
                    ("The password must contain at least 1 uppercase letter, A-Z."),
                    code='password_no_upper',
                )
            if not re.findall('[a-z]', data):
                raise ValidationError(
                    ("The password must contain at least 1 lowercase letter, a-z."),
                    code='password_no_lower',
                )
            if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', data):
                raise ValidationError(
                    ("The password must contain at least 1 special character: " +
                        "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"),
                    code='password_no_symbol',
                )

            return data
    
    
class Verify_OTP_serializer(serializers.Serializer):
        email = serializers.CharField(required=True)
        name = serializers.CharField(required=True)
        user_name = serializers.CharField(required=True)
        password = serializers.CharField(required=True)
        
        def create(self,validated_data):
            return OTP.objects.create(**validated_data)
        
        def validate_password(self, data):
            if len(data) < 8 :
                raise ValidationError(
                    ("The password needs to be more than 8 characters")
                )
            
            if not re.findall('\d', data):
                raise ValidationError(
                    ("The password must contain at least 1 digit, 0-9."),
                    code='password_no_number',
                )
            if not re.findall('[A-Z]', data):
                raise ValidationError(
                    ("The password must contain at least 1 uppercase letter, A-Z."),
                    code='password_no_upper',
                )
            if not re.findall('[a-z]', data):
                raise ValidationError(
                    ("The password must contain at least 1 lowercase letter, a-z."),
                    code='password_no_lower',
                )
            if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', data):
                raise ValidationError(
                    ("The password must contain at least 1 special character: " +
                        "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"),
                    code='password_no_symbol',
                )

            return data