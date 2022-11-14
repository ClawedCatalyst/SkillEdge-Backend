from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *
from base.models import *
from base.api.serializers import *
from .pagination import PaginationHandlerMixin
from rest_framework.pagination import PageNumberPagination
from .filters import CourseFilter
from moviepy.editor import VideoFileClip
import math  
from .rating import calculate_weighted_rating
# from pymediainfo import MediaInfo
# import cv2
# import datetime
# import subprocess
# import json


class Category_view(APIView):
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

    def get(self,request):
        categories = interests.objects.all()
        serializer = categorySerializer(categories, many=True)
        
        return Response(serializer.data)
        
class Course_view(APIView):

    def get(self,request):
        data = Course.objects.all()
        data = Course.objects.order_by('-weighted_rating')
        serializer = TopicSerializer(data, many=True)
        return Response(serializer.data) 


    permission_classes = [IsAuthenticated,]
    def post(self,request):
        email = request.user.email
        user = NewUserRegistration.objects.get(email__iexact=email)
        request.POST._mutable = True
        request.data["educator_mail"] = request.user.id
        request.data["educator_name"] = user.name
        request.POST._mutable = False
        if user.is_educator == True:
            serializer = TopicSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)    
        else:
            return Response({'msg':'user is not an educator'})   

 
class Basic_pagination(PageNumberPagination):
    page_size_query_param = 'limit'            

class View_filtered_courses(APIView, PaginationHandlerMixin):
    permission_classes = [IsAuthenticated,]
    pagination_class = Basic_pagination
    serializer_class = TopicSerializer
    def get(self,request):
        email = request.user.email
        user = NewUserRegistration.objects.get(email__iexact=email)
        user_interested_courses = user.interested.all()
        courses = Course.objects.filter(category__in=user_interested_courses)
        
        courses = Course.objects.order_by('-weighted_rating')
        page = self.paginate_queryset(courses)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,many=True).data)
        else:
            serializer = self.serializer_class(courses, many=True)
        
        return Response(serializer.data)

class Course_rating(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self,request):
        email = request.user.email
        user = NewUserRegistration.objects.get(email__iexact=email)
        history = feedbackmodel.objects.filter(user = user.name,course=request.data.get('course'))
        if len(history)!=0:
            return Response({'msg':'you already gave your review for this course'})
        request.POST._mutable = True
        request.data["sender"] = user.id
        request.data["user"] = user.name
        request.POST._mutable = False
        seri = GetRatingSerializer(data=request.data)
        if seri.is_valid(raise_exception=True):
            # ck = feedbackmodel.objects.latest('time')
            course_id= request.data.get("course")
            course= Course.objects.get(id=course_id)
            count = course.review_count
            rating = course.rating
            seri.save()
            rating_serializer = RatingSerializer(instance = course,data=request.data)
            if rating_serializer.is_valid(raise_exception=True):
                rating_serializer.save()
                review = course.latest_review
                # return Response(check)
                if count == 0:
                    rating_serializer = RatingSerializer(instance = course,data=request.data)
                    if rating_serializer.is_valid(raise_exception=True):
                        course.rating = review
                        course.review_count = 1
                        course.weighted_rating = calculate_weighted_rating(course)
                        rating_serializer.save()
                        return Response({'msg':'Thanks for your review'})
                else:
                    present_rating = rating*count
                    new_rating = (present_rating + review)/(count + 1)
                    count+=1
                    course.review_count = count
                    rating_serializer = RatingSerializer(instance = course,data=request.data)
                    if rating_serializer.is_valid(raise_exception=True):
                        course.rating = new_rating
                        course.weighted_rating = calculate_weighted_rating(course)
                        rating_serializer.save()
                        return Response({'msg':'Thanks for your review'})
                return Response({'msg':'Something went wrong'})
            # rating_serializer = RatingSerializer(instance = course,data=request.data)
            # if rating_serializer.is_valid(raise_exception=True):
            #     rating_serializer.save()
            #     return Response(rating)
            return Response({'msg':'enter valid details'})

class Searching(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self,request):
        queryset = Course.objects.all()
        my_filter = CourseFilter(request.GET, queryset=queryset)
        queryset = my_filter.qs
        
        search_result = request.GET.get('search-area') or ''
        
        if search_result:
            queryset = queryset.filter(topic__icontains=search_result)
            
        serializer = TopicSerializer(queryset, many=True)
        
        if serializer.data == []:
            return Response({'msg':'Nothing Found'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.data)  
    
class Purchased_courses(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self,request):
        email = request.user.email
        user = NewUserRegistration.objects.get(email__iexact=email)
        array = user.purchasedCourse.all()
        courses = Course.objects.filter(id__in=array)
        topic_serializer = TopicSerializer(courses, many=True)
        return Response(topic_serializer.data)
    

class Lesson_view(APIView):
    permission_classes = [IsAuthenticated,]
    
    def get(self,request):
        lesson = lessons.objects.all()
        serializer = lessonSerializer(lesson, many=True)
        
        return Response(serializer.data)
    
    
    
    def post(self,request):
        email = request.user.email
        user = NewUserRegistration.objects.get(email__iexact=email)
        topic = request.data.get("topic")
        course = Course.objects.get(id=topic)
        
        if str(course.educator_mail) != str(email):
            return Response({'msg':'invalid'})
        
        try:
            print(course.educator_mail)
            print(email)
            if user.is_educator == True:
                    request.POST._mutable = True
                    request.data["topic"] = topic
                    request.POST._mutable = False
                    serializer = lessonSerializer(data=request.data)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                        # media_info = MediaInfo.parse(serializer.data['file'])
                        # length = media_info.tracks[0].duration
                        
                        # video = VideoFileClip(str(serializer.data['file']))
                        # print(serializer.data['file'])
                        # length = video.duration
                        # print(length)
                        # seconds = math.floor(length%60)
                        # seconds = seconds/100
                        # minutes = math.floor(length//60)   
                        
                        
                        # print(minutes+seconds)
                    # lesson_id = lessons.objects.get(id=serializer.data['id'])
                    # lesson_id.length = str(duration_seconds)
                    # lesson_id.save()
                    
                    return Response({'msg':'lesson added'})    
            return Response({'msg':'user is not an educator'})
        except:
            return Response({'msg':'invalid'}, status=status.HTTP_400_BAD_REQUEST)     
        
    
class View_specific_course_lesson(APIView):
    def post(self,request):
        try:
            topic = request.data.get("topic")
            lesson = lessons.objects.filter(topic=topic)
            serializer = lessonSerializer(lesson, many=True)
            if serializer.data == []:
                return Response({"msg":"No such course exists"},status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data)
        except:
            return Response({"msg":"Enter a valid course"}, status=status.HTTP_400_BAD_REQUEST)  
            
class Course_feedback(APIView):
    def get(self,request,ck):
        course = feedbackmodel.objects.filter(course = ck)
        rating_serializer = GetRatingSerializer(instance = course , many = True)
        return Response(rating_serializer.data)