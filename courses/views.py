from re import search
from unicodedata import category
from rest_framework import status
from logging import raiseExceptions
from educator import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *
from base.models import *
from base.api.serializers import *
from rest_framework import filters
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import PaginationHandlerMixin
from rest_framework.pagination import PageNumberPagination


class AddCategoryUser(APIView):
    permission_classes = [IsAuthenticated,]
    def put(self,request):
        email = request.user.email
        user = NewUserRegistration.objects.get(email__iexact=email)
        serializer = catSerializer(data=request.data)

        if serializer.is_valid():
            for i in range(11):
                s = 'Interest' + str(i+1)
                if serializer.data[s] == True:
                    gettingCategory = interests.objects.get(id=i + 1)
                    user.interested.add(gettingCategory)
        else:
            return Response({'msg':'Invalid Entry'}, status=status.HTTP_400_BAD_REQUEST)            
        
        serializer = profileSerializer(user, many=False)

        return Response(serializer.data)
        


class ViewAllCategories(APIView):
    def get(self,request):
        categories = interests.objects.all()
        serializer = categorySerializer(categories, many=True)
        
        return Response(serializer.data)

class ViewAllCourses(APIView):
    def get(self,request):
        data = Course.objects.all()
        serializer = TopicSerializer(data, many=True)
        return Response(serializer.data)


class CourseView(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self,request):
        email = request.user.email
        user = NewUserRegistration.objects.get(email__iexact=email)
        if user.is_educator == True:
            serializer = TopicSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)    
        else:
            return Response({'msg':'user is not an educator'})    

class CourseRating_calci(APIView):
    def post(self,request,ck):
            course = Course.objects.get(id=ck)
            count = course.review_count
            rating = course.rating
            ser = RatingSerializer(instance = course,data=request.data)
            if ser.is_valid(raise_exception=True):
                ser.save()
                review = course.latest_review
                # return Response(check)
                if count == 0:
                    ser = RatingSerializer(instance = course,data=request.data)
                    if ser.is_valid(raise_exception=True):
                        course.rating = review
                        course.review_count = 1
                        ser.save()
                        return Response({'msg':'Thanks for your review'})
                else:
                    present_rating = rating*count
                    new_rating = (present_rating + review)/(count + 1)
                    count+=1
                    course.review_count = count
                    ser = RatingSerializer(instance = course,data=request.data)
                    if ser.is_valid(raise_exception=True):
                        course.rating = new_rating
                        ser.save()
                        return Response({'msg':'Thanks for your review'})
                return Response({'msg':'Something went wrong'})
            # ser = RatingSerializer(instance = course,data=request.data)
            # if ser.is_valid(raise_exception=True):
            #     ser.save()
            #     return Response(rating)
            return Response({'msg':'enter valid details'})
 
class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'            

class viewFilteredCourses(APIView, PaginationHandlerMixin):
    permission_classes = [IsAuthenticated,]
    pagination_class = BasicPagination
    serializer_class = TopicSerializer
    def get(self,request):
        email = request.user.email
        user = NewUserRegistration.objects.get(email__iexact=email)
        array = user.interested.all()
        courses = Course.objects.filter(category__in=array)
        
        page = self.paginate_queryset(courses)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,many=True).data)
        else:
            serializer = self.serializer_class(courses, many=True)
        
        return Response(serializer.data)
        
        
class CourseRating(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self,request):
        email = request.user.email
        user = NewUserRegistration.objects.get(email__iexact=email)
        seri = GetRatingSerializer(data=request.data)
        if seri.is_valid(raise_exception=True):
            seri.save()
            ck = feedbackmodel.objects.latest('time')
            course=ck.course
            count = course.review_count
            rating = course.rating
            ser = RatingSerializer(instance = course,data=request.data)
            if ser.is_valid(raise_exception=True):
                ser.save()
                review = course.latest_review
                # return Response(check)
                if count == 0:
                    ser = RatingSerializer(instance = course,data=request.data)
                    if ser.is_valid(raise_exception=True):
                        course.rating = review
                        course.review_count = 1
                        ser.save()
                        return Response({'msg':'Thanks for your review'})
                else:
                    present_rating = rating*count
                    new_rating = (present_rating + review)/(count + 1)
                    count+=1
                    course.review_count = count
                    ser = RatingSerializer(instance = course,data=request.data)
                    if ser.is_valid(raise_exception=True):
                        course.rating = new_rating
                        ser.save()
                        return Response({'msg':'Thanks for your review'})
                return Response({'msg':'Something went wrong'})
            # ser = RatingSerializer(instance = course,data=request.data)
            # if ser.is_valid(raise_exception=True):
            #     ser.save()
            #     return Response(rating)
            return Response({'msg':'enter valid details'})

class searching(generics.ListCreateAPIView):

    queryset = Course.objects.all()
    serializer_class = TopicSerializer
    search_fields = ['topic','short_description']
    filter_backends = (filters.SearchFilter,DjangoFilterBackend)
    filterset_fields = ['category','price']
     
        

        