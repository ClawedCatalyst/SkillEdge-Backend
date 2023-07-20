from dataclasses import field

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from base.models import *

from .models import *


class CartSerializer(ModelSerializer):
    class Meta:
        model = cart
        fields = ["email", "user"]

        extra_kwargs = {"email": {"required": True}}


class AddCartSerializer(ModelSerializer):
    class Meta:
        model = cart_courses
        fields = ["cart", "course"]

        extra_kwargs = {"course": {"required": False}, "cart": {"required": False}}
