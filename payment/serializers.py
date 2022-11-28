from rest_framework import serializers
from base.models import *
from .models import *
from django.core.exceptions import ValidationError

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        
    def validate(self,data):
        user = NewUserRegistration.objects.get(email=data["user_mail"])
        user.wallet += int(data["order_amount"])
        if user.wallet < 0:
            raise ValidationError(
                    ({'msg':'Not enough Balance'})
                )
        user.save()
        
        return data    