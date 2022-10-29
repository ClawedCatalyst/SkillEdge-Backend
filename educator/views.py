from base.models import NewUserRegistration
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from base.models import *
from base.api.serializers import *
from educator.form import *
from educator.serializers import *


class BecomeEducator(APIView):
    def put(self, request, pk):
        user = NewUserRegistration.objects.get(id=pk)
        
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
        
class AddCourse(APIView):
    def post(self, request, pk):
        user = NewUserRegistration.objects.get(id=pk)
        form = catform()
        if request.method == 'POST':
            form = catform(request.POST)
            if form.is_valid():
                form.save()
        ser = TopicSerializer(instance=user, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        # if request.method == 'POST':
        #     form = catform(request.POST)
        #     if form.is_valid():
        #         form.save()
        #         return render({'msg':'course hosted'},status=status.HTTP_400_GOOD_REQUEST)
        return Response({'msg':'course not hosted'},status=status.HTTP_400_BAD_REQUEST)