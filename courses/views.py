from email import message_from_binary_file
from unicodedata import category
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *
from base.models import *
from base.api.serializers import *
from rest_framework.pagination import PageNumberPagination
from .filters import CourseFilter
import math  
from .rating import calculate_weighted_rating
from rest_framework import generics
from django.contrib.postgres.search import TrigramWordSimilarity, TrigramSimilarity,SearchVector
from django.db.models.functions import Greatest


class Category_view(APIView):
    permission_classes = [IsAuthenticated,]
    def put(self,request):
        user = NewUserRegistration.objects.get(email=request.user.email)
        serializer = addInterestSerializer(user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
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
        if user.is_educator == True:
            all_courses = Course.objects.filter(educator_mail = request.user.id)
            total_weighted_rating = 0.0
            for each_course in all_courses:
                total_weighted_rating += each_course.weighted_rating
            if len(all_courses) == 0:
                avg_weighted_rating=0
            else:
                avg_weighted_rating = total_weighted_rating/len(all_courses)
            user.educator_rating = avg_weighted_rating
            user.save()
            if avg_weighted_rating >= 2.5:
                user.is_certified_educator = True
                user.save()
                request.POST._mutable = True
                request.data["educator_mail"] = request.user.id
                request.data["educator_name"] = user.name
                request.POST._mutable = False
                serializer = TopicSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data) 
            else:
                user.is_certified_educator = False
                user.save()    
                request.POST._mutable = True
                request.data["educator_mail"] = request.user.id
                request.data["educator_name"] = user.name
                request.data["price"] = 0
                request.POST._mutable = False
                serializer = TopicSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data) 
        else:
            return Response({'msg':'user is not an educator'})   


class Course_rating(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self,request):
        email = request.user.email
        user = NewUserRegistration.objects.get(email__iexact=email)
        check_status = 0
        history = feedbackmodel.objects.filter(user = user.name,course=request.data.get('course'))
        if len(history)!=0:
            check_status = 1
            history.delete()
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
                        if check_status == 0:
                            return Response({'msg':'Thanks for your review'})
                        if check_status == 1:
                            return Response({'msg':'Review edited: Thanks for your review'})
                else:
                    present_rating = rating*count
                    new_rating = (present_rating + review)/(count + 1)
                    if check_status == 0:
                        count+=1
                    course.review_count = count
                    rating_serializer = RatingSerializer(instance = course,data=request.data)
                    if rating_serializer.is_valid(raise_exception=True):
                        course.rating = new_rating
                        course.weighted_rating = calculate_weighted_rating(course)
                        rating_serializer.save()
                        if check_status == 0:
                            return Response({'msg':'Thanks for your review'})
                        if check_status == 1:
                            return Response({'msg':'Review edited: Thanks for your review'})
                return Response({'msg':'Something went wrong'})
            # rating_serializer = RatingSerializer(instance = course,data=request.data)
            # if rating_serializer.is_valid(raise_exception=True):
            #     rating_serializer.save()
            #     return Response(rating)
            return Response({'msg':'enter valid details'})

    def get(self,request,ck):
        email = request.user.email
        user = NewUserRegistration.objects.get(email__iexact=email)
        feedback = feedbackmodel.objects.filter(course=ck,sender=request.user.id)
        if len(feedback)==0:
            return Response({"msg":"Not rated"}, status=status.HTTP_400_BAD_REQUEST)  
        print(feedback)
        feedback_serializer = GetRatingSerializer(instance = feedback, many=True)
        return Response(feedback_serializer.data)

class Purchased_courses(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self,request):
        email = request.user.email
        user = NewUserRegistration.objects.get(email__iexact=email)
        array = user.purchasedCourse.all()
        courses = Course.objects.filter(id__in=array)
        topic_serializer = TopicSerializer(courses, many=True)
        return Response(topic_serializer.data)
    

# class Lesson_view(APIView):
#     permission_classes = [IsAuthenticated,]
    
#     def get(self,request):
#         lesson = lessons.objects.all()
#         serializer = lessonSerializer(lesson, many=True)
        
#         return Response(serializer.data)
    
    
    
#     def post(self,request):
#         email = request.user.email
#         user = NewUserRegistration.objects.get(email__iexact=email)
#         topic = request.data.get("topic")
#         course = Course.objects.get(id=topic)
        
#         if str(course.educator_mail) != str(email):
#             return Response({'msg':'invalid'})
        
#         try:
#             print(course.educator_mail)
#             print(email)
#             if user.is_educator == True:
#                     request.POST._mutable = True
#                     request.data["topic"] = topic
#                     request.POST._mutable = False
#                     serializer = lessonSerializer(data=request.data)
#                     if serializer.is_valid(raise_exception=True):
#                         serializer.save()
#                     return Response({'msg':'lesson added'})    
#             return Response({'msg':'user is not an educator'})
#         except:
#             return Response({'msg':'invalid'}, status=status.HTTP_400_BAD_REQUEST)     
    
    
# class View_specific_course_lesson(APIView):
#     def post(self,request):
#         try:
#             topic = request.data.get("topic")
#             lesson = lessons.objects.filter(topic=topic)
#             serializer = lessonSerializer(lesson, many=True)
#             if serializer.data == []:
#                 return Response({"msg":"No such course exists"},status=status.HTTP_400_BAD_REQUEST)
#             return Response(serializer.data)
#         except:
#             return Response({"msg":"Enter a valid course"}, status=status.HTTP_400_BAD_REQUEST)  

        
                   
            
class Course_feedback(APIView):
    def get(self,request,ck):
        course = feedbackmodel.objects.filter(course = ck)
        rating_serializer = GetRatingSerializer(instance = course , many = True)
        return Response(rating_serializer.data)
    


#View Filtered Courses Based On Interest API
    
class View_filtered_courses(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TopicSerializer
    paginate_by = 10
    def get_queryset(self):
        return Course.objects.filter(category__in=self.request.user.interested.all()).order_by('-weighted_rating')


#Searching API 
    
class Searching(generics.ListAPIView):
    serializer_class = TopicSerializer
    def get_queryset(self):
        queryset = Course.objects.all()
        my_filter = self.request.GET.get('my_filter')
        if my_filter is not None:
            queryset = queryset.filter(category=my_filter)
        
        search_result = self.request.GET.get('search-area') or ''
        return queryset.annotate(similarity=Greatest( TrigramWordSimilarity(search_result, 'topic'), TrigramWordSimilarity(search_result, 'educator_name'))).filter(similarity__gt=0.30).order_by('-similarity')  


# Create Lesson API
    
class Lesson_view(generics.CreateAPIView):
        serializer_class =  lessonSerializer
        permission_classes = [IsAuthenticated]    
        
        def post(self, request):
            return self.create(request)     
           
#Lesson View Of a Particular Course API

class View_specific_course_lesson(generics.ListAPIView):
    serializer_class = lessonSerializer
    lesson = lessons.objects.all()
    def get_queryset(self):
        topic = self.request.data.get("topic")
        return self.lesson.filter(topic=topic)
                