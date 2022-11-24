from dataclasses import field
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *
from base.models import *

class TopicSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ['id','category','topic','educator_mail','short_description','thumbnail','price','rating','educator_name']
        
class categorySerializer(ModelSerializer):
    class Meta:
        model = interests 
        fields = ['id','interest']
        
class AddcategorySerializer(ModelSerializer):
    class Meta:
        model = interests
        fields = ['email']               
        fields = ['id','category','topic','educator_mail','short_description','thumbnail','price','rating','review_count','latest_review']

class RatingSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ['latest_review']

        extra_kwargs = {'latest_review': {'required': True}}

class GetRatingSerializer(ModelSerializer):
    class Meta:
        model = feedbackmodel
        fields = ['course','latest_review','comment','sender','user']

        extra_kwargs = {'course': {'required': True},'latest_review': {'required': False}}

    
class lessonSerializer(ModelSerializer):
    class Meta:
        model = lessons
        fields = ['id','topic','lessonName','file','length']    
        
class AddLessonSerializer(ModelSerializer):
    
    class Meta:
        model = lessons
        fields = ['id','topic','lessonName','file']        