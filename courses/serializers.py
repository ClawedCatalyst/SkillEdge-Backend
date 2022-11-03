from dataclasses import field
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *

class TopicSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ['id','category','topic','educator_mail','short_description','thumbnail','price']
        
class categorySerializer(ModelSerializer):
    class Meta:
        model = category 
        fields = ['id','category','email']
        
class AddcategorySerializer(ModelSerializer):
    class Meta:
        model = category
        fields = ['email']               
        fields = ['id','category','topic','educator_mail','short_description','thumbnail','price','rating','review_count','latest_review']

class RatingSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ['latest_review']

        extra_kwargs = {'latest_review': {'required': True}}

class catSerializer(serializers.Serializer):
    Interest1 = serializers.BooleanField()
    Interest2 = serializers.BooleanField()
    Interest3 = serializers.BooleanField()
    Interest4 = serializers.BooleanField()
    Interest5 = serializers.BooleanField()
    Interest6 = serializers.BooleanField()
    Interest7 = serializers.BooleanField()
    Interest8 = serializers.BooleanField()
    Interest9 = serializers.BooleanField()
    Interest10 = serializers.BooleanField()
    Interest11 = serializers.BooleanField()