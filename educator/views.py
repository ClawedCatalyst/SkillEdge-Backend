from base.models import NewUserRegistration
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from base.models import *
from base.api.serializers import *
from educator.serializers import *
from courses.models import *
from courses.serializers import *


class BecomeEducator(APIView):
    permission_classes = [IsAuthenticated,]
    def put(self, request):
        email = request.user.email
        user = NewUserRegistration.objects.get(email__iexact=email)
        
        if user.is_verified == True:
            if user.is_educator == False:
                user.is_educator = True
                user.save()
                serializer = profileSerializer(user, many=False)
                return Response(serializer.data)
            else:
                return Response({'msg':'user is already a educator'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'msg':'user is not verified'}, status=status.HTTP_400_BAD_REQUEST)    

    def get(self, request):
        email = request.user.email
        educator = NewUserRegistration.objects.get(email__iexact=email)
        courses = Course.objects.filter(educator_mail = educator.id)
        serializer = TopicSerializer(courses, many=True)
        return Response(serializer.data)


        