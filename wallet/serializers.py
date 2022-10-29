from dataclasses import field
from rest_framework.serializers import ModelSerializer
from .models import *
from base.models import *
from educator.models import *
from courses.models import *

class GetEducatorSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ['educator_mail','price']

class WalletSerializer(ModelSerializer):
    class Meta:
        model = NewUserRegistration
        fields = ['wallet']