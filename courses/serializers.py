from dataclasses import field
from rest_framework.serializers import ModelSerializer
from .models import *

class TopicSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ['id','category','topic','educator_mail','short_description','thumbnail','price','rating']

class RatingSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ['rating']