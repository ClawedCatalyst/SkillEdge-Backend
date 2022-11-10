from dataclasses import field
from base.models import NewUserRegistration
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

class NewUserSerializer(ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = NewUserRegistration
        fields = ["id","name","user_name", "email", "password", "confirm_password", "is_verified","is_educator","wallet"]
        extra_kwargs={
            'password':{'write_only': True},
        }
    
    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        
        if password != confirm_password :
            raise serializers.ValidationError("Password doesn't match")
        
        return data
    
    def create(self, validate_data):
        return NewUserRegistration.objects.create_user(**validate_data)
    

class loginSerializer(ModelSerializer):
    class Meta:
        model = NewUserRegistration
        fields = ["email","password"]


class profileSerializer(ModelSerializer):
    class Meta:
        model = NewUserRegistration
        fields = ("name", "user_name" ,"picture", "gender","dateOfBirth","mobile","is_educator","email",)
        
        extra_kwargs = {'email': {'required': False ,"allow_null": True},}
    

class otpcheckserializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

class resetpassserializer(serializers.Serializer):
    email = serializers.EmailField()

class passchangeserializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    passwordd = serializers.CharField()
    confirm_passwordd = serializers.CharField()