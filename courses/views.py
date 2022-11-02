from logging import raiseExceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *
from base.models import *



class ViewAllCourses(APIView):
    def get(self,request):
        data = Course.objects.all()
        serializer = TopicSerializer(data, many=True)
        return Response(serializer.data)


class CourseView(APIView):
    def post(self,request,pk):
        user = NewUserRegistration.objects.get(id=pk)
        if user.is_educator == True:
            serializer = TopicSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)    
        else:
            return Response({'msg':'user is not an educator'})    

class CourseRating(APIView):
    def post(self,request,ck):
        ser = RatingSerializer(data=request.data)
        if ser.is_valid(raise_exception=True):
            course = Course.objects.get(id=ck)
            count = course.review_count
            rating = course.rating
            if count == 0:
                rating = ser.data['rating']
                count = 1
                return Response({'msg':'Thanks for your review'})

            else:
                present_rating = rating*count
                new_rating = (present_rating + ser.data['rating'])/(count + 1)
                count+=1    
                return Response({'msg':'Thanks for your review'})
            return Response({'msg':'Something went wrong'})
        return Response({'msg':'enter valid details'})
            



        
