from base.models import NewUserRegistration
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from base.models import *
from base.api.serializers import *
from educator.serializers import *
from courses.models import *
from courses.serializers import *


class BecomeEducator(APIView):
    permission_classes = [IsAuthenticated,]
    def put(self, request):
        email = request.educator.email
        educator = NewUserRegistration.objects.get(email__iexact=email)
        
        if educator.is_verified == True:
            if educator.is_educator == False:
                educator.is_educator = True
                educator.save()
                serializer = profileSerializer(educator, many=False)
                return Response(serializer.data)
            else:
                return Response({'msg':'educator is already a educator'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'msg':'educator is not verified'}, status=status.HTTP_400_BAD_REQUEST)    

    def get(self, request):
        email = request.educator.email
        educator = NewUserRegistration.objects.get(email__iexact=email)
        courses = Course.objects.filter(educator_mail = educator.id)
        serializer = TopicSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        email = request.user.email
        educator = NewUserRegistration.objects.get(email__iexact=email)
        all_courses = Course.objects.filter(educator_mail = request.user.id)
        if educator.is_verified == True:
            if educator.is_educator == True:
                total_weighted_rating = 0.0
                for each_course in all_courses:
                    total_weighted_rating += each_course.weighted_rating
                print(total_weighted_rating)
                avg_weighted_rating = total_weighted_rating/len(all_courses)
                print(avg_weighted_rating)
                educator.educator_rating = avg_weighted_rating
                educator.save()
                if avg_weighted_rating  >= 2.5:
                    return Response({'msg':'You are a certified educator'}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'msg':'You are not a certified educator'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'msg':'user is not a educator'}, status=status.HTTP_400_BAD_REQUEST)                
        return Response({'msg':'user is not verified'}, status=status.HTTP_400_BAD_REQUEST)

        