from dataclasses import field
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *
from base.models import *

class CartSerializer(ModelSerializer):
    class Meta:
        model = cart
        fields = ['student_mail']

        extra_kwargs = {'student_mail': {'required': True}}
        

class AddCartSerializer(ModelSerializer):
    class Meta:
        model = cart_courses
        fields = ['cart','course']

        extra_kwargs = {'course': {'required': True},'cart': {'required': True} }