from django.shortcuts import render
from rest_framework import status
from logging import raiseExceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from courses.serializers import *
from .models import *
from base.models import *
from rest_framework import generics

# View Courses In Cart
class Get_cart(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = TopicSerializer
    def get_queryset(self):
        cart_id = cart.objects.get(user = self.request.user.id)
        courses = cart_courses.objects.filter(cart=cart_id.id).values_list('course')
        if len(courses) == 0:
            return Response({'msg':'no courses in cart'}, status=status.HTTP_400_BAD_REQUEST)
        return Course.objects.filter(id__in=courses)

# Add Course To Cart
class Post_cart(generics.CreateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = AddCartSerializer
    def post(self,request):
        request.data.update({"cart" : cart.objects.get(user =request.user.id).id})
        cart_course = cart_courses.objects.filter(cart=request.data["cart"],course=request.data["course"])
        if len(cart_course) == 0:
            super().create(request)
            return Response({'msg':'course added successfully to cart'})
        return Response({'msg':'course already added to cart'}, status=status.HTTP_400_BAD_REQUEST)

# Remove Course From Cart
class Cart(APIView):
    permission_classes = [IsAuthenticated,]
    def delete(self,request,ck):
        user = NewUserRegistration.objects.get(email__iexact= request.user.email)
        cart_id = cart.objects.get(user = request.user.id)
        cart_courseid = cart_courses.objects.filter(cart=cart_id.id,course=ck)
        if len(cart_courseid)==0:
            return Response({'msg':'course does not exist in cart'}, status=status.HTTP_400_BAD_REQUEST)
        cart_id.total_price -= Course.objects.get(id=ck).price
        cart_courseid.delete()
        cart_id.save()
        return Response({'msg':'course removed successfully from cart'})

# Create your views here.
# class Create_cart(APIView):
#     permission_classes = [IsAuthenticated,]
#     def post(self,request):
#         email = request.user.email
#         serializer = CartSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response({'msg':'cart added successfully'})

# class Cart_id(APIView):
#     permission_classes = [IsAuthenticated,]
#     def get(self,request):
#         email = request.user.email
#         cart_details = cart.objects.get(email__iexact =email)
#         cart_id = cart_details.id
#         return Response(cart_id)


    # def put(self,request):
    #     try:
    #         email = request.user.email
    #         user = NewUserRegistration.objects.get(email__iexact=email)
    #         course_array = user.purchasedCourse.all()
    #         course_id = request.data.get("course")
    #         course_details = Course.objects.get(id = course_id)
    #         educator = course_details.educator_mail
    #         if user.id == educator.id:
    #                 return Response({'msg':'You can not buy your self hosted course '}, status=status.HTTP_400_BAD_REQUEST)
    #         for course in course_array:
    #             if (course.id==int(course_id)) :
    #                 return Response({'msg':'course already purchased'}, status=status.HTTP_400_BAD_REQUEST)
    #         cart_details = cart.objects.get(email__iexact =email)
    #         cart_id = cart_details.id
    #         request.POST._mutable = True
    #         request.data["cart"] = cart_id
    #         request.POST._mutable = False
    #         serializer = AddCartSerializer(data=request.data)
    #         if serializer.is_valid(raise_exception=True):
    #             # data =request.data
    #             carts=request.data.get("cart")
    #             course=request.data.get("course")
    #             cart_course = cart_courses.objects.filter(cart=carts,course=course)
    #             l = len(cart_course)
    #             if l == 0:
    #                 serializer.save()
    #                 return Response({'msg':'course added successfully to cart'})
    #             else:
    #                 return Response({'msg':'course already added to cart'}, status=status.HTTP_400_BAD_REQUEST)
            
    #     except:
    #         return Response({'msg':'Invalid method'}, status=status.HTTP_400_BAD_REQUEST)

    # def get(self,request):
    #         email = request.user.email
    #         user = NewUserRegistration.objects.get(email__iexact=email)
    #         cart_id = cart.objects.get(email__iexact =email)
    #         # print(ct.id)
    #         courses = cart_courses.objects.filter(cart=cart_id.id)
    #         # print(courses)
    #         if len(courses) == 0:
    #             return Response({'msg':'no courses in cart'}, status=status.HTTP_400_BAD_REQUEST)
    #         else:
    #             courselist= []
    #             for course in courses:
    #                 cid = course.course.id
    #                 crs = Course.objects.get(id=cid)
    #                 serializer = TopicSerializer(instance = crs)
    #                 # print(serializer.data)
    #                 courselist.append(serializer.data)

    #         # serializer = TopicSerializer(instance = courselist, many = True)
    #         return Response(courselist)

# class Delete_in_cart(generics.RetrieveDestroyAPIView):
#     permission_classes = [IsAuthenticated,]
#     serializer_class = AddCartSerializer
#     lookup_url_kwarg = 'ck'
#     def get_queryset(self):
#         cid=cart.objects.get(user =self.request.user.id).id
#         print(cart_courses.objects.filter(cart=cid,course=self.request.GET.get('course-id')))
#         return cart_courses.objects.filter(cart=cid,course=self.request.GET.get('course-id')) 

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         self.perform_destroy(instance)

        
# email = request.user.email
#         course_details = Course.objects.get(id = request.data['course'])
#         if request.user.id == course_details.educator_mail.id:
#             return Response({'msg':'You can not buy your self hosted course '}, status=status.HTTP_400_BAD_REQUEST)
#         course = user.purchasedCourse.get(course=request.data['course'])
#         if course.exists():
#             return Response({'msg':'course already purchased'}, status=status.HTTP_400_BAD_REQUEST)   
#         request.POST._mutable = True
#         request.data["cart"] = cart.objects.get(email__iexact =email).id
#         request.POST._mutable = False
#         carts=request.data.get("cart")
#         course=request.data.get("course")
#         cart_course = cart_courses.objects.filter(cart=carts,course=course)
#         l = len(cart_course)
#         if l == 0:
#             self.create(request)
#             return Response({'msg':'course added successfully to cart'})
#         else:
#             return Response({'msg':'course already added to cart'}, status=status.HTTP_400_BAD_REQUEST)
