from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *



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
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        else:
            return Response({'msg':'user is not an educator'})    
            