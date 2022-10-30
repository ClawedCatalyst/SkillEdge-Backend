from base.models import NewUserRegistration
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from base.models import *
from base.api.serializers import *
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
        