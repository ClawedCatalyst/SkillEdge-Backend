# from ast import Return
# import json
# from urllib import response

# import environ
# import razorpay

import email
from .models import Order
from rest_framework import status
from base.models import *
from .serializers import OrderSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from base.models import *
from rest_framework import generics

# env = environ.Env()
# environ.Env.read_env()

# # start_payment


# class startPayment(APIView):
#         permission_classes = [IsAuthenticated,]
#         def post(self,request):
#         # request.data is coming from frontend
#             amount = request.data['amount']
#             name = request.data['name']

#             # setup razorpay client this is the client to whome user is paying money that's you
#             client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))

#             # create razorpay order
#             # the amount will come in 'paise' that means if we pass 50 amount will become
#             # 0.5 rupees that means 50 paise so we have to convert it in rupees. So, we will 
#             # mumtiply it by 100 so it will be 50 rupees.
#             payment = client.order.create({"amount": int(amount) * 100, 
#                                             "currency": "INR", 
#                                             "payment_capture": "1"})

#             # we are saving an order with isPaid=False because we've just initialized the order
#             # we haven't received the money we will handle the payment succes in next 
#             # function
#             order = Order.objects.create(order_product=name, 
#                                             order_amount=amount, 
#                                             order_payment_id=payment['id'])

#             serializer = OrderSerializer(order)

#             """order response will be 
#             {'id': 17, 
#             'order_date': '23 January 2021 03:28 PM', 
#             'order_product': '**product name from frontend**', 
#             'order_amount': '**product amount from frontend**', 
#             'order_payment_id': 'order_G3NhfSWWh5UfjQ', # it will be unique everytime
#             'isPaid': False}"""

#             email = request.user.email
#             user = NewUserRegistration.objects.get(email=email)
#             user.wallet += int(order.order_amount)
#             user.save()
            
#             data = {
#                 "payment": payment,
#                 "order": serializer.data,
#                 "walletAmount": user.wallet
#             }
#             return Response(data)

# # handle_payment_success

# class handle_payment_success(APIView):
#     permission_classes = [IsAuthenticated,]
#     def post(self,request):
#         # request.data is coming from frontend
#         razorpay_pay_id =  request.data["razorpay_pay_id"]
#         razorpay_ord_id =  request.data["razorpay_ord_id"]
#         razorpay_signat = request.data["razorpay_signat"]
       
#         res = {
#            'razorpay_payment_id': razorpay_pay_id,
#            'razorpay_order_id': razorpay_ord_id,
#            'razorpay_signature': razorpay_signat
#         }
       
       
#         """
#         res will be:
#         {'razorpay_payment_id': 'pay_G3NivgSZLx7I9e', 
#         'razorpay_order_id': 'order_G3NhfSWWh5UfjQ', 
#         'razorpay_signature': '76b2accbefde6cd2392b5fbf098ebcbd4cb4ef8b78d62aa5cce553b2014993c0'}
#         this will come from frontend which we will use to validate and confirm the payment
#         """

#         ord_id = ""
#         raz_pay_id = ""
#         raz_signature = ""

#         # res.keys() will give us list of keys in res
#         for key in res.keys():
#             if key == 'razorpay_order_id':
#                 ord_id = res[key]
#             elif key == 'razorpay_payment_id':
#                 raz_pay_id = res[key]
#             elif key == 'razorpay_signature':
#                 raz_signature = res[key]

#         # get order by payment_id which we've created earlier with isPaid=False
#         order = Order.objects.get(order_payment_id=ord_id)

#         # we will pass this whole data in razorpay client to verify the payment
#         data = {
#             'razorpay_order_id': ord_id,
#             'razorpay_payment_id': raz_pay_id,
#             'razorpay_signature': raz_signature
#         }

#         client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))

#         # checking if the transaction is valid or not by passing above data dictionary in 
#         # razorpay client if it is "valid" then check will return None
#         check = client.utility.verify_payment_signature(data)

#         if check is not None:
#             print("Redirect to error url or error page")
#             return Response({'error': 'Something went wrong'})

#         # if payment is successful that means check is None then we will turn isPaid=True
#         order.isPaid = True
#         order.save()
#         email = request.user.email
#         user = NewUserRegistration.objects.get(email=email)
#         user.wallet += int(order.order_amount)


#         res_data = {
#             'message': 'payment successfully received!'
#         }

#         return Response(res_data)

# class Flutter_Razorpay(APIView):
#     permission_classes = [IsAuthenticated,]
    
#     def get(self, request):
#         email = request.user.email
#         user = NewUserRegistration.objects.get(email=email)
#         transaction_history = Order.objects.filter(user_mail=user.id)
#         serializer = OrderSerializer(transaction_history, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         try:
#             email = request.user.email
#             user = NewUserRegistration.objects.get(email=email)
#             request.POST._mutable = True
#             request.data["user_mail"] = request.user.id
#             request.POST._mutable = False
#             serializer = OrderSerializer(data=request.data)
#             if serializer.is_valid(raise_exception=True):
#                 serializer.save()
#                 print(user.wallet)
#                 user.wallet += int(serializer.data['order_amount'])
#                 if user.wallet < 0:
#                     return Response({'msg':'Not enough Balance'}, status=status.HTTP_400_BAD_REQUEST)
                
#                 user.save()
#                 print(user.wallet)
#                 return Response(serializer.data)
#         except:
#             return Response({"msg":"Payment Failed"}, status=status.HTTP_400_BAD_REQUEST)    

class Flutter_Razorpay(generics.ListAPIView,generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user_mail=self.request.user.id)
    
    def post(self,request):
        request.data["user_mail"] = request.user.id
        return self.create(request)