from dataclasses import field
from rest_framework.serializers import ModelSerializer
from educator.models import *

class TopicSerializer(ModelSerializer):
    class Meta:
        model = topic
        fields = '__all__'