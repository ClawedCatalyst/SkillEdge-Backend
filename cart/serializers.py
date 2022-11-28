from dataclasses import field
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *
from base.models import *
from django.core.exceptions import ValidationError

class CartSerializer(ModelSerializer):
    class Meta:
        model = cart
        fields = ['email','user']

        extra_kwargs = {'email': {'required': True}}
        

class AddCartSerializer(ModelSerializer):
    class Meta:
        model = cart_courses
        fields = ['cart','course']

        extra_kwargs = {'course': {'required': False},'cart': {'required': False} }

    def to_representation(self, instance):
        email = self.request.user.email
        ret = super().to_representation(instance)
        cart_details = cart.objects.get(email__iexact =email)
        ret['cart'] = cart_details.id
        print(ret)
        return ret

    def validate(self,data):
        course_details = Course.objects.get(id = data['course'])
        if self.context['request'].user.id == course_details.educator_mail.id:
            raise ValidationError(
                ({'msg':'You can not buy your self hosted course '})
                )
        course = user.purchasedCourse.get(course=data['course'])
        if course.exists():
            raise ValidationError(
                ({'msg':'course already purchased'})
                )       
        return data