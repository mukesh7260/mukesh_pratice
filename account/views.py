from contextlib import nullcontext
from genericpath import exists
import json
from site import addsitedir
from tkinter import EW             # sudo apt-get install python3-tk
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from adsapi.models import Product,LastLogin,QrCode
from blogsapi.models import Blogs
from adsapi.serializers import ProductSerializer
from account.serializers import *
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
import random
import http.client
from paymentapi.models import TransationIdone
import datetime
from pytz import timezone 

from profileapi.models import Profile
from .models import *
import ast
from adsapi.models import Pricing,PaymentDetailsValues

# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = get_tokens_for_user(user)
    return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

# class UserLoginView(APIView):
#   renderer_classes = [UserRenderer]
#   def post(self, request, format=None):
#     serializer = UserLoginSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     email = serializer.data.get('email')
#     password = serializer.data.get('password')
#     user = authenticate(email=email, password=password)
#     if user is not None:
#       token = get_tokens_for_user(user)
#       # added this line for last login
#       user_login_time, created = UserLoginTime.objects.get_or_create(user=user)

#         # Store the previous login time
#       previous_login_time = user_login_time.login_time

#         # Update the login_time with the current time
#       user_login_time.login_time = timezone.now()

#         # Update the previous_login_time with the previous login time
#       user_login_time.previous_login_time = previous_login_time

#       user_login_time.save()

#       return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
#     else:
#       return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    max_allowed_devices=3
    if user is not None:
       # Check the number of active devices for the user
      active_devices_count_before_increment = user.active_devices
      # print("Active Devices Count before increment:", active_devices_count_before_increment)
      # Log out the oldest session if the user has reached the device limit
     
      if active_devices_count_before_increment >= max_allowed_devices:
        # Get the oldest session based on the login time
         oldest_session = User.objects.filter(name=user.name).order_by('created_at').first()
         if oldest_session:
            print("Is Oldest session expired:", oldest_session.is_token_expired())
            # Check if the oldest session has expired
            if oldest_session.is_token_expired():
                print("Oldest session has expired. Deleting...")
                print("Deleted session info:", {
            'token_value': oldest_session.token_key,
            'expiration_time': oldest_session.token_expiration_time ,
            'created_at': oldest_session.created_at,
            'device_info': oldest_session.active_devices
        })
                oldest_session.delete()
                print(oldest_session)
                print("Oldest session has expired. Deleted session info:", oldest_session)
               
               
            else:
                print("Oldest session has not expired.")


      # Genaerate Token for new User ####
      token = get_tokens_for_user(user)
      print("Token Created:", token)


       # Update the devices count for the user using F object
       # Update the devices count for the user
      # Increment the devices count for the user
      user.active_devices += 1
      user.save()


      print("Active Devices Count after increment:", user.active_devices)
      # Try to retrieve or create UserLoginTime
      try:
        user_login_time, created = UserLoginTime.objects.get_or_create(user=user)
      except UserLoginTime.DoesNotExist:
        # Handle the case where the user does not have a UserLoginTime record
        user_login_time = None
        created = False
      # added this line for last login
      if user_login_time is not None:
        print("User Login Time:", user_login_time.login_time)


        # Store the previous login time
        previous_login_time = user_login_time.login_time


        # Update the login_time with the current time
        user_login_time.login_time = timezone.now()


        # Update the previous_login_time with the previous login time
        user_login_time.previous_login_time = previous_login_time


        user_login_time.save()


      return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
 
class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)


from django.core import serializers

class userads(APIView):
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    print(request.user.id)
    adsData=Product.objects.filter(user =request.user)
    print("adsData",adsData)
    serializer = serializers.serialize('json', adsData)
    print(serializer)
    qs_json = serializers.serialize('json', adsData)
    return HttpResponse(qs_json, content_type='application/json')

# class userblogs(APIView):
#   permission_classes = [IsAuthenticated]
#   def post(self, request, format=None):
#     print(request.user.id)
#     blogsData=Blogs.objects.filter(user =request.user)
#     print("blogsData",blogsData)
#     serializer = serializers.serialize('json', blogsData)
#     print(serializer)
#     qs_json = serializers.serialize('json', blogsData)
#     return HttpResponse(qs_json, content_type='application/json')
from blogsapi.serializers import BlogsSerializer
class userblogs(APIView):
    def get(self, request):
        blogs = Blogs.objects.all()
        serializer = BlogsSerializer(blogs, many=True)
        return Response(serializer.data)
      
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = BlogsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class wishlist(APIView):
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    wishlist=request.data.get('wishlist')
    print("wishlist ",wishlist,type("wishlist"),len(wishlist))

    
    if (len(wishlist) == 0):
      print("len is zerop")
      newlist=[]
    else:
      wishlist=wishlist+","
      newlist=[]
      y=""
      for x in wishlist:
        if x!=",":
          y=y+x
        else:
          newlist.append(int(y))
          print("value",newlist)
          y=""
          print(newlist)

    wishlist=Product.objects.filter(pk__in=newlist)
    print("@@findal dat in wishlist ",wishlist)
    wishlist = serializers.serialize('json', wishlist)
    return HttpResponse(wishlist, content_type='application/json')




class updateProfile1(APIView):
  def post(self, request, format=None):
    email=request.data.get("email")
    s=Profile.objects.filter(email=email)
    print(type(s))
    if(s):
      profile = serializers.serialize('json', s)
      return HttpResponse(profile, content_type='application/json')
    return HttpResponse("false", content_type='application/json')

class createFeatured(APIView):
  def post(self, request, format=None):
    image=request.data.get("image")
    user=request.data.get("user")
    title=request.data.get("title")
    price=request.data.get("price")
    tags=request.data.get("tags")
    description=request.data.get("description")
    category=request.data.get("category")
    brand=request.data.get("brand")
    condition=request.data.get("condition")
    state=request.data.get("state")
    city=request.data.get("city")
    locality=request.data.get("locality")
    zip_code=request.data.get("zip_code")
    # date_created=request.data.get("date_created")
    # video=request.data.get("video")
    is_featured=True
    is_active=False
    token=request.data.get("token")
    print(token)
    # print("success value",self.request.session["success"])
    s1=TransationIdone.objects.filter(id1=token)
    print("9999999999999999999999999999999999999999",s1)
    if s1:
      if("succ" in token):
        print("success")
        s=Product.objects.create(image=image,user_id=user,title=title,tags=tags,price=price,description=description,category=category,brand=brand,condition=condition,state=state,city=city,locality=locality,zip_code=zip_code,is_featured=is_featured,is_active=is_active)
        s.save()
        s1=TransationIdone.objects.get(id1=token)
        print(s.pk)
        print("fsedjklfjoisdpljufkl;dsfjkldsfjkl;esdjflksddfjdskl")
        s1.adsid_id=s.pk
        s1.userid_id=user
        s1.save()
      else:
        print("fail path")
        return HttpResponse("fail", content_type='application/json')
    else:
      return HttpResponse("fail", content_type='application/json')
    
    return HttpResponse("success", content_type='application/json')


class ordersPyament(APIView):
  def post(self,request,format=None):
    user=request.data.get("user")
    order=request.data.get("order")
    payment=request.data.get("payment")
    print(order)
    
    s1=Product.objects.filter(user_id=user)
    s=TransationIdone.objects.filter(userid_id=user)
    data = serializers.serialize('json', s1)
    print(data)
    # return HttpResponse(data,content_type='application/json')
    
      
    
    s=TransationIdone.objects.filter(userid_id=user)
    
    # return HttpResponse("unable to fetch",)
    for x in s:
      s1=Product.objects.filter(id=x.adsid_id)
      if s1:
        x.ProductData=serializers.serialize('json', s1)
      data = serializers.serialize('json', s)
      return HttpResponse(data,content_type='application/json')



class verifyEmail(APIView):
    def post(self,request,format=None):
      email=request.data.get("email")
      s=User.objects.filter(email=email)
      if s:
        return HttpResponse("already exist",content_type='application/json')
      else:
        return HttpResponse("not exist",content_type='application/json')



class verifyPhone(APIView):
    def post(self,request,format=None):
      phoneNumber=request.data.get("phoneNumber")
      print(phoneNumber)
      # s1=User.objects.filter(email=email)
      # s=User.objects.filter(phoneNumber=phoneNumber)
      try:
        user = User.objects.get(phoneNumber=phoneNumber)
      except:
        user=None
      if user is not None:
        token = get_tokens_for_user(user)
        return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
      else:
        return Response({'errors':{'non_field_errors':['phone Number not exist']}}, status=status.HTTP_404_NOT_FOUND)
class verifyEmailLogin(APIView):
    def post(self,request,format=None):
      email=request.data.get("email")
      print(email)
      # s1=User.objects.filter(email=email)
      # s=User.objects.filter(phoneNumber=phoneNumber)
      try:
        user = User.objects.get(email=email)
      except:
        user=None
      if user is not None:
        token = get_tokens_for_user(user)
        return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
      else:
        return Response({'errors':{'non_field_errors':['Email not exist']}}, status=status.HTTP_404_NOT_FOUND)
class viewsupdate(APIView):
    def post(self, request, format=None):
        adsID= request.data.get("adsID")
        s = Product.objects.get(pk=adsID)
        s.viewsproduct = s.viewsproduct+1
        s.save()
        return HttpResponse("success", content_type='application/json')          

# class updateProfileApi(APIView):
#     def post(self, request, format=None):
#         user = request.data.get("user")
#         print(user)
#         if user is None:
#           print('address')
#           idvalues=request.data.get("idvalues")
#           try:
#             s=Profile.objects.filter(user_id=idvalues)
#             data = serializers.serialize('json', s)
#             return HttpResponse(data, content_type='application/json') 
#           except:
#             s=None
#             return HttpResponse("Not exist", content_type='application/json') 
#         else:
#               image = request.data.get("image")
#               user = request.data.get("user")
#               name = request.data.get("name")
#               email = request.data.get("email")
#               PhoneNumber = request.data.get("PhoneNumber")
#               print(PhoneNumber)
#               address = request.data.get("address")
#               state = request.data.get("state")
#               city =request.data.get("city")
#               zipcode = request.data.get("zipcode")
#               print(Profile.objects.filter(user_id=user))
#               if Profile.objects.filter(user_id=user) :
#                 s=Profile.objects.get(user_id=user)
#                 s.image=image
#                 s.name=name
#                 s.email=email
#                 s.PhoneNumber=PhoneNumber
#                 s.address=address
#                 s.state=state
#                 s.city=city
#                 s.zipcode=zipcode
#                 s.save()
#               else:
#                 userID = User.objects.get(pk=user)
#                 s=Profile.objects.create(image=image,user=userID,city=city,name=name,email=email,PhoneNumber=PhoneNumber,address=address,state=state,zipcode=zipcode,)
#                 s.save()
#               return HttpResponse("success", content_type='application/json') 

import base64
from django.core.exceptions import ObjectDoesNotExist

class updateProfileApi(APIView):
    def post(self, request, format=None):
        user_id = request.data.get("user")

        if user_id is None:
            idvalues = request.data.get("idvalues")
            try:
                profile = Profile.objects.get(user_id=idvalues)
                data = serializers.serialize('json', [profile])
                return HttpResponse(data, content_type='application/json') 
            except ObjectDoesNotExist:
                return HttpResponse("Not exist", content_type='application/json')
        else:
            image = request.data.get("image")
            image_base64 = None
            if image:
                try:
                    # Check if the file is an in-memory file
                    if hasattr(image, 'read'):
                        image_base64 = base64.b64encode(image.read()).decode("utf-8")
                    else:
                        # Otherwise, treat it as a regular file
                        with open(image.path, "rb") as f:
                            image_base64 = base64.b64encode(f.read()).decode("utf-8")
                except FileNotFoundError:
                    pass  # Handle the file not found exception if necessary

            name = request.data.get("name")
            email = request.data.get("email")
            PhoneNumber = request.data.get("PhoneNumber")
            address = request.data.get("address")
            state = request.data.get("state")
            city = request.data.get("city")
            zipcode = request.data.get("zipcode")

            try:
                profile = Profile.objects.get(user_id=user_id)
                profile.image = image
                profile.name = name
                profile.email = email
                profile.PhoneNumber = PhoneNumber
                profile.address = address
                profile.state = state
                profile.city = city
                profile.zipcode = zipcode
                profile.image_base64 = image_base64
                profile.save()
            except ObjectDoesNotExist:
                user_instance = User.objects.get(pk=user_id)
                profile = Profile.objects.create(
                    image=image,
                    user=user_instance,
                    city=city,
                    name=name,
                    email=email,
                    PhoneNumber=PhoneNumber,
                    address=address,
                    state=state,
                    zipcode=zipcode,
                    image_base64=image_base64,
                )
                profile.save()

            return HttpResponse("success", content_type='application/json')

class userProfileDetailsApi(APIView):
    def post(self, request, format=None):
        user1 = request.data.get("user")
        s=User.objects.filter(pk=user1)   
        data = serializers.serialize('json', s)
        return HttpResponse(data,content_type='application/json')     

class lastLoginTime(APIView):
    def post(self, request, format=None):
        user1 = request.data.get("user")
        currentDateTime= datetime.datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
        print("start")
        checkUserExit=LastLogin.objects.filter(userlogin_id=user1)
        print("end")
        if checkUserExit:
          print("first")
          checkUserExit=LastLogin.objects.get(userlogin_id=user1)
          checkUserExit.lastloginValue=currentDateTime
          checkUserExit.save()
          print(checkUserExit)
          data = serializers.serialize('json', LastLogin.objects.filter(userlogin_id=checkUserExit.userlogin_id))
          return HttpResponse(data,content_type='application/json') 
        else:
          print("second")
          s=LastLogin.objects.create(userlogin_id=user1,lastloginValue=currentDateTime)
          s.save()
          print(s.pk)
          data = serializers.serialize('json', LastLogin.objects.filter(userlogin_id=s.userlogin_id))
          return HttpResponse(data,content_type='application/json')    


# class lastLoginTimeGet(APIView):
#   def post(self, request, format=None):
#       user1 = request.data.get("user")
#       data = serializers.serialize('json', LastLogin.objects.filter(userlogin_id=user1))
#       return HttpResponse(data,content_type='application/json')  
from django.utils import timezone
import pytz
from datetime import datetime

# class lastLoginTimeGet(APIView):
#   def post(self, request, format=None):
#       user1 = request.data.get("user")
#       try:
#             # Attempt to retrieve the LastLogin record for the specified user
#             last_login_datetime = LastLogin.objects.get(userlogin_id=user1)
#       except LastLogin.DoesNotExist:
#             # If the record doesn't exist, create a new one
#             last_login_datetime= LastLogin(userlogin_id=user1)
#       # Get the current time in the 'Asia/Kolkata' time zone
#       asia_kolkata = pytz.timezone('Asia/Kolkata')
#       current_time_kolkata = datetime.now(asia_kolkata)
#       # Format the time in the desired time zone as a string
#       current_datetime = current_time_kolkata.strftime('%Y-%m-%d %H:%M:%S.%f')      
#       # Update the lastloginValue field with the current timestamp
#       last_login_datetime.lastloginValue = current_datetime
#       last_login_datetime.save()
#       # Serialize and return the updated record in JSON format
#       data = serializers.serialize('json', LastLogin.objects.filter(userlogin_id=user1))
#       # data = serializers.serialize('json', [last_login_datetime])
#       return HttpResponse(data,content_type='application/json')  
from django.http import JsonResponse
from pytz import timezone as pytz_timezone  # Import pytz to work with time zones

# class lastLoginTimeGet(APIView):
#     def post(self, request):
#         user_id = request.POST.get('user')
#         try:
#             user_login_time = UserLoginTime.objects.get(user_id=user_id)
#             last_login_time = user_login_time.login_time
            
#             if last_login_time:
#                 kolata_timezone = pytz_timezone('Asia/Kolkata')
#                 last_login_time = last_login_time.astimezone(kolata_timezone)
                
#                 response_data = [
#                     {
#                         "model": "adsapi.lastlogin",
#                         "pk": user_login_time.id,  # Assuming you want the primary key of UserLoginTime as 'pk'
#                         "fields": {
#                             "userlogin": str(user_id),  # Convert user_id to a string
#                             "lastloginValue": last_login_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
#                         }
#                     }
#                 ]
#             else:
#                 response_data = {'message': 'No last login time available for this user.'}
#             return JsonResponse(response_data, safe=False)
#         except UserLoginTime.DoesNotExist:
#             response_data = {'message': 'User not found.'}
#             return JsonResponse(response_data, status=404)
from django.http import JsonResponse
from pytz import timezone as pytz_timezone  # Import pytz to work with time zones


class lastLoginTimeGet(APIView):
    def post(self, request, format=None):
        user_id = request.data.get("user_id")


        if user_id is None:
            return Response({"error": "User ID is missing"}, status=status.HTTP_400_BAD_REQUEST)


        try:
            user_id = int(user_id)
        except ValueError:
            return Response({"error": "Invalid user ID"}, status=status.HTTP_400_BAD_REQUEST)


        try:
            user_instance = User.objects.get(id=user_id)
            last_login_datetime, created = LastLogin.objects.get_or_create(userlogin=user_instance)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except LastLogin.DoesNotExist:
            last_login_datetime = LastLogin(userlogin=user_instance)


        asia_kolkata = pytz.timezone('Asia/Kolkata')
        current_time_kolkata = datetime.now(asia_kolkata)
        current_datetime = current_time_kolkata.strftime('%Y-%m-%d %H:%M:%S.%f')


        # Check if there's a previous login time
        if last_login_datetime.lastloginValue:
            # Update the lastloginValue field with the previous last login time
            previous_last_login_time = last_login_datetime.lastloginValue
            last_login_datetime.lastloginValue = previous_last_login_time
        else:
            # If there's no previous login time, set lastloginValue to the current time
            last_login_datetime.lastloginValue = current_datetime


        # Update the previous_login_time field with the current last login time
        last_login_datetime.previous_login_time = current_datetime


        last_login_datetime.save()


        data = {
            "userlogin": user_id,
            "lastloginValue": last_login_datetime.lastloginValue,
            # "previous_login_time": last_login_datetime.previous_login_time
        }


        return Response(data, status=status.HTTP_200_OK)
      
import qrcode
from PIL import Image
import os
import base64
class QrCodeAds(APIView):
  def post(self, request, format=None):
        product= request.data.get("product")
        Logo_link = 'C:/Users/91910/Downloads/compressed_filename/hola9DjangoLatest/adsapi/hola9.png'

        logo = Image.open(Logo_link)

        # taking base width
        basewidth = 100

        # adjust image size
        wpercent = (basewidth/float(logo.size[0]))
        hsize = int((float(logo.size[1])*float(wpercent)))
        # logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
        logo = logo.resize((basewidth, hsize), Image.LANCZOS)  # Use Image.LANCZOS instead of Image.ANTIALIAS

        QRcode = qrcode.QRCode(
	        error_correction=qrcode.constants.ERROR_CORRECT_H
        )

        # taking url or text
        url = 'https://hola9.com/ads-listing/'+product

        # adding URL or text to QRcode
        QRcode.add_data(url)

        # generating QR code
        QRcode.make()

        # taking color name from user
        QRcolor = 'black'

        # adding color to QR code
        QRimg = QRcode.make_image(
	    fill_color=QRcolor, back_color="white").convert('RGB')

        # set size of QR code
        pos = ((QRimg.size[0] - logo.size[0]) // 2,
	        (QRimg.size[1] - logo.size[1]) // 2)
        QRimg.paste(logo, pos)

        # save the QR code generated
        QRimg.save('C:/Users/91910/Downloads/compressed_filename/hola9DjangoLatest/adsapi/gfg_QR.png')
        logo1 = Image.open("C:/Users/91910/Downloads/compressed_filename/hola9DjangoLatest/adsapi/gfg_QR.png")
        print(logo1)
        file_path = os.path.join("C:/Users/91910/Downloads/compressed_filename/hola9DjangoLatest/adsapi/", "gfg_QR.png")
        with open("C:/Users/91910/Downloads/compressed_filename/hola9DjangoLatest/adsapi/gfg_QR.png", "rb") as image_file:
          encoded_string = base64.b64encode(image_file.read())
        s=QrCode.objects.create(image=encoded_string,product_id=product)
        return HttpResponse("Success", content_type='application/json')

class getQrCodeAds(APIView):
  def post( self,request, format=None):
    product =request.data.get("product")
    s=QrCode.objects.filter(product_id=product)
    data = serializers.serialize('json', s)
    return HttpResponse(data, content_type='application/json')

class reviewSection(APIView):
    def get(self, request, format=None):
      review=ReviewSection.objects.all().order_by("-id")[0:5]
      data = serializers.serialize('json', review)
      return HttpResponse(data , content_type='application/json')
    
   
class TrackingTele(APIView):
  def post( self,request, format=None):
    teleData =request.data.get("data")
    data=ast.literal_eval(teleData)
    teleId=data["id"]
    print(teleId)
    if(TelemetryDaa.objects.filter(teleId=teleId)):
      details=TelemetryDaa.objects.get(teleId=teleId)
      objDetails=ast.literal_eval(details.data)
      print(details.data)
      print(data)
      # code for form handling in telemetry obj
      for x in data["form"]:
        if x in objDetails.keys():
            objDetails[x].append(data["form"][x])
        else:
          
          objDetails["form"][x]=data["form"][x]
          print(x)
          print(data)
          print(objDetails)
      # end of this obj form telemetry 
      for x in data["product"]:
        objDetails["product"].append(x)
      if(data==ast.literal_eval(details.data)):
        print("equal")
      else:
        print("not equal")
        for val in data["views"]:
          if val in objDetails["views"]:
            objDetails["views"][val]=objDetails["views"][val] + data["views"][val]
          else:
            objDetails["views"][val]=data["views"][val]
        #for views updating
        # if data["views"].keys() == objDetails["views"].keys():
        #   print("views equal keys")
        #   for key in objDetails["views"]:
        #     objDetails["views"][key]=objDetails["views"][key]+data["views"][key]    
        #   print("views equal keys",objDetails["views"])
        # else:
        #   print("views not equalt keys")
        print(objDetails)
        details.data=json.dumps(objDetails)
        details.save()

    else:
      objDetails=ast.literal_eval(teleData)
      print("data is their ",objDetails)
      s=TelemetryDaa.objects.create(data=teleData,teleId=teleId)
      s.save()
      print("create details",s)
      
    return HttpResponse("success", content_type='application/json')
  def get(self, request, format=None):
    s=TelemetryDaa.objects.all()
    data = serializers.serialize('json', s)
    return HttpResponse(data , content_type='application/json')
import ast
class PaymentDetails(APIView):
  def post( self,request, format=None):
    paymentDetails = request.data.get("paymentDetails")
    print(type(request.data.get("paymentDetails")))
    print(request.data.get("paymentDetails"))
    # paymentDetails=ast.literal_eval(request.data.get("paymentDetails"))
    print(paymentDetails["UserID"])
    print(type(paymentDetails["UserID"]))
    pricingiD=None
    user=paymentDetails["UserID"]
    OrderID=paymentDetails["orderid"]
    category =paymentDetails["plan"]["category"]
    days =paymentDetails["plan"]["days"]
    regulars =paymentDetails["plan"]["regulars"]
    topAds =paymentDetails["plan"]["topAds"]
    featured=paymentDetails["plan"]["featured"]
    teleSupport=paymentDetails["plan"]["teleSupport"]
    response=paymentDetails["plan"]["response"]
    chatSupport=paymentDetails["plan"]["chatSupport"]
    dedicatedRm=paymentDetails["plan"]["dedicatedRm"]
    hol9Website=paymentDetails["plan"]["hola9Website"]
    print("sending--------------------------------")
    
    s=Pricing.objects.create(user_id=user,category=category,days=days,regulars=regulars,topAds=topAds,featured=featured,teleSupport=teleSupport,response=response,chatSupport=chatSupport,dedicatedRm=dedicatedRm,hol9Website=hol9Website,OrderID=OrderID)
    s.save()
    if False:
      s=Pricing.objects.get(user_id=user)
      s.category=category
      s.featured_ads=featured_ads
      s.ads_limit=ads_limit
      s.ads_timing=ads_timing
      s.top_listing=top_listing
      s.support=support
      s.adsLeft=adsLeft
      s.save()
      pricingiD=s.pk
    else:
      if paymentDetails["plan"]["category"]=="Free":
        s=Pricing.objects.create(user_id=user,category=category,days=days,regulars=regulars,topAds=topAds,featured=featured,teleSupport=teleSupport,response=response,chatSupport=chatSupport,dedicatedRm=dedicatedRm,hol9Website=hol9Website,OrderID=OrderID)
        s.save()
        pricingiD=s.pk
    # s1=PaymentDetailsValues.objects.create(UserValue_id=paymentDetails["UserID"],PlanValue_id=pricingiD,OrderValue_id=paymentDetails["orderid"])
    # s1.save()
    # print("s.id is printing ........................................",s1)
    return HttpResponse("Success",content_type='application/json') 




# class jobDetails(APIView):
#   def post(self, request, format=None):
#     serializer = jobdetailsSerializers(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     user = serializer.save()
#     applied = get_tokens_for_user(user)
#     return Response("Sucess",content_type='application/json')

# class jobDetails(APIView):
 
#     def get(self, request):
#         job_applications = JobApply.objects.all()
#         serializer = jobdetailsSerializers(job_applications, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = jobdetailsSerializers(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         applied = get_tokens_for_user(user)
#         return Response("Sucess",content_type='application/json')
from rest_framework import generics

class jobDetails(generics.ListCreateAPIView):
    serializer_class = jobdetailsSerializers
    def get_queryset(self):  
            limit = self.request.query_params.get('limit', None)
            queryset = JobApply.objects.all()
            if limit:
                # If only "limit" parameter is provided, order by id and limit the queryset
                queryset = queryset.order_by('-id')[:int(limit)]
            return queryset
            # serializer = self.get_serializer(queryset, many=True)
            # return Response(serializer.data)
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
      
    def post(self, request, *args, **kwargs):
        serializer = jobdetailsSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
      
class JobDetailsUpdateDelete(APIView):
    def get_object(self, pk):
        try:
            return JobApply.objects.get(pk=pk)
        except JobApply.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        job = self.get_object(pk)
        serializer = jobdetailsSerializers(job)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        job = self.get_object(pk)
        serializer = jobdetailsSerializers(job, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        job = self.get_object(pk)
        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class jobsRequired(APIView):
  def post(self,request, formate=None):
      serializer = jobsRequiredSerialize(data=request.data)
      serializer.is_valid(raise_exception=True)
      user = serializer.save()
      s=JobsRequired.objects.all()
      data = serializers.serialize('json', s)
      return HttpResponse(data, content_type='application/json')
  def get(self,request, formate=None):
      s=JobsRequired.objects.all()
      data = serializers.serialize('json', s)
      return HttpResponse(data, content_type='application/json')

class FullProfile(APIView):
    def post( self,request , format=None):
        userId=request.data.get("user")
        for x in Profile.objects.all():
          print(x.user_id)
        profileData=Profile.objects.filter(user=userId)
        print(profileData)
        data = serializers.serialize('json', profileData)
        return HttpResponse(data, content_type='application/json')
      
      

      
from rest_framework import generics
class EnquiryListCreate(generics.ListCreateAPIView):
    queryset = ContactForm.objects.all()
    serializer_class = ContactSerializer




from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Contact
from .serializers import ContactEnquireSerializer

class ContactListView(APIView):
    def get(self, request):
        contacts = Contact.objects.all()
        serializer = ContactEnquireSerializer(contacts, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = ContactEnquireSerializer(data=request.data)
        if serializer.is_valid():
            # Check if a resume file was uploaded
            if 'resume' in request.data:
                # Get the uploaded file
                uploaded_file = request.data['resume']

                # Convert the file to base64
                try:
                    base64_encoded = base64.b64encode(uploaded_file.read()).decode('utf-8')
                except Exception as e:
                    return Response({'error': 'Error encoding file to base64.'}, status=status.HTTP_400_BAD_REQUEST)

                # Update the serializer's data to store the base64 encoded resume
                serializer.validated_data['resume_base64'] = base64_encoded

            serializer.save()  # Save the data to the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # def post(self, request):
    #     serializer = ContactEnquireSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EmployeeLogin

class EmployeeLoginView(APIView):
    def post(self,request,format=None):
        username = request.data.get("username")
        password = request.data.get("password")
        name = request.data.get("name")
        x = EmployeeLogin.objects.filter(username=username).filter(password=password).filter(name=name)
        if x:
            return HttpResponse("true", content_type='application/json')
        else:
            return HttpResponse("false", content_type='application/json')


# class EmployeeDetailsView(APIView):
#     def post(self,request,format=None):
#         serializer = EmployeeDetailsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Data Submitted Successfully!"},status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

import base64
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import EmployeeDetails
from .serializers import EmployeeDetailsSerializer

class EmployeeDetailsView(APIView):
    def post(self, request, format=None):
        serializer = EmployeeDetailsSerializer(data=request.data)
        if serializer.is_valid():
            # Check if a document file was uploaded
            if 'documnet' in request.data:
                # Get the uploaded file
                uploaded_file = request.data['documnet']

                # Convert the file to base64
                try:
                    base64_encoded = base64.b64encode(uploaded_file.read()).decode('utf-8')
                except Exception as e:
                    return Response({'error': 'Error encoding file to base64.'}, status=status.HTTP_400_BAD_REQUEST)

                # Update the serializer's data to store the base64 encoded document
                serializer.validated_data['document_base64'] = base64_encoded

            serializer.save()  # Save the data to the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class EmployeeProfileView(APIView):
    def get(self,requets):
        emp_profile = EmployeeDetails.objects.all()
        serializer = EmployeeDetailsSerializer(emp_profile,many=True)
        return Response(serializer.data)
      

      
# from rest_framework import generics
# from .models import EmployeeDetails
# from .serializers import EmployeeDetailsSerializer
# from rest_framework.response import Response
# from rest_framework import status

# class EmployeeProfileView(generics.ListAPIView):
#     queryset = EmployeeDetails.objects.all()
#     serializer_class = EmployeeDetailsSerializer

#     def get(self, request):
#         # Get the EmployeeDetails objects and serialize them
#         employee_details = self.get_queryset()
#         serializer = self.get_serializer(employee_details, many=True)

#         # Extract specific fields from the serialized data
#         response_data = []
#         for item in serializer.data:
#             employee_data = {
#                 "name": item.get("name"),
#                 "task": item.get("task"),
#                 "task_date": item.get("task_date"),
#                 "report_of_work": item.get("report_of_work"),
#                 "completion_status": item.get("completion_status"),
#                 "documnet": item.get("documnet"),
#                 "comment": item.get("comment"),
#             }
#             response_data.append(employee_data)

#         return Response(response_data, status=status.HTTP_200_OK)



from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view

# @api_view(['GET', 'POST'])
# def review_section_list(request):
#     if request.method == 'GET':
#         review_sections = ReviewSection.objects.all()
#         serializer = ReviewSectionSerializer(review_sections, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = ReviewSectionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST'])
def review_section_list(request):
    if request.method == 'GET':
        limit = request.query_params.get('limit', None)

        if limit is not None and limit.isdigit():
            review_sections = ReviewSection.objects.all()[:int(limit)]
        else:
            review_sections = ReviewSection.objects.all()

        serializer = ReviewSectionSerializer(review_sections, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ReviewSectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def review_section_detail(request, pk):
    review_section = get_object_or_404(ReviewSection, pk=pk)

    if request.method == 'GET':
        serializer = ReviewSectionSerializer(review_section)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ReviewSectionSerializer(review_section, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        review_section.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# from rest_framework.decorators import api_view


# @api_view(['GET', 'POST'])
# def review_section_list(request):
#     if request.method == 'GET':
#         review_sections = ReviewSection.objects.all()
#         serialized_data = []
#         for review_section in review_sections:
#             serialized_data.append({
#                 "model": "account.reviewsection",
#                 "pk": review_section.pk,
#                 "fields": {
#                     "title": review_section.title,
#                     "description": review_section.description,
#                     "profile": review_section.profile,
#                     "role": review_section.role,
#                     "rating": review_section.rating,
#                     "image": review_section.image,
#                     "created_at": review_section.created_at.isoformat()  # Format the date
#                 }
#             })
#         return Response(serialized_data)

#     elif request.method == 'POST':
#         serializer = ReviewSectionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def review_section_detail(request, pk):
#     review_section = get_object_or_404(ReviewSection, pk=pk)

#     if request.method == 'GET':
#         serialized_data = {
#             "model": "account.reviewsection",
#             "pk": review_section.pk,
#             "fields": {
#                 "title": review_section.title,
#                 "description": review_section.description,
#                 "profile": review_section.profile,
#                 "role": review_section.role,
#                 "rating": review_section.rating,
#                 "image": review_section.image,
#                 "created_at": review_section.created_at.isoformat()  # Format the date
#             }
#         }
#         return Response(serialized_data)

#     # Rest of the view code remains the same for PUT and DELETE requests.




class LoginProfileList(APIView):
    def get(self, request):
        # Retrieve all user profiles
        profiles = LoginProfile.objects.all()
        serializer = LoginProfileSerializer(profiles, many=True)
        return JsonResponse(serializer.data, safe=False)

    # def post(self, request):
    #     serializer = LoginProfileSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    #     return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request, format=None):
        serializer = LoginProfileSerializer(data=request.data)
        if serializer.is_valid():
            # Check if a document file was uploaded
            if 'image' in request.data:
                # Get the uploaded file
                uploaded_file = request.data['image']

                # Convert the file to base64
                try:
                    base64_encoded = base64.b64encode(uploaded_file.read()).decode('utf-8')
                except Exception as e:
                    return Response({'error': 'Error encoding file to base64.'}, status=status.HTTP_400_BAD_REQUEST)

                # Update the serializer's data to store the base64 encoded document
                serializer.validated_data['image_base64'] = base64_encoded

            serializer.save()  # Save the data to the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Contact
from .serializers import ContactEnquireSerializer
from django.db.models import Max

class ContactEnquireAPIView(APIView):
    def post(self, request, format=None):
        # Get the parameters from the request
        limit = request.data.get('limit')
        name = request.data.get('name', None)
        qualification = request.data.get('qualification', None)
        posted_by = request.data.get('posted_by', None)
        percentage = request.data.get('percentage', None)
        date_of_birth = request.data.get('date_of_birth', None)
        phone_number = request.data.get('phone_number', None)
        jobtitle = request.data.get('jobtitle', None)
        ads_id = request.data.get('ads_id', None)
        company_name = request.data.get('company_name', None)
        try:
            # Validate and convert input values to integers
            limit = int(limit) if limit is not None else None
        except ValueError:
            return JsonResponse({'error': 'Invalid input values'}, status=400)
        # Start with the entire queryset
        queryset = Contact.objects.all()

        # Apply filters based on parameters
        if name:
            queryset = queryset.filter(name=name)
        if qualification:
            queryset = queryset.filter(qualification=qualification)
        if posted_by:
            queryset = queryset.filter(posted_by=posted_by)
        if percentage:
            queryset = queryset.filter(percentage=percentage)
        if date_of_birth:
            queryset = queryset.filter(date_of_birth=date_of_birth)
        if phone_number:
            queryset = queryset.filter(phone_number=phone_number)
        if jobtitle:
            queryset = queryset.filter(jobtitle=jobtitle)
        if ads_id:
            queryset = queryset.filter(ads_id=ads_id)
        if company_name:
            queryset = queryset.filter(company_name=company_name)

        # If limit is provided, get the latest IDs
        if limit:
            queryset = queryset.order_by('-id')[:limit]


        serializer = ContactEnquireSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




from django.http import Http404

class ProfileList1(APIView):
    def get(self, request):
        user_id = request.query_params.get('user', None)
        
        if user_id is not None:
            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                raise Http404("User does not exist")
            
            profiles = Profile.objects.filter(user=user)
            total_fields = Profile._meta.fields  # Get all fields of the Profile model
            total_fields_count = len(total_fields)
            
            # Fields to exclude from the calculation
            excluded_fields = ['user', 'image_base64']
            
            # Count the number of filled fields in all profiles
            filled_fields_count = 0
            for profile in profiles:
                for field in total_fields:
                    if field.name not in excluded_fields:
                        field_value = getattr(profile, field.attname)
                        if field_value is not None and field_value != "" and str(field_value).lower() != "null":
                            filled_fields_count += 1
            
            # Calculate percentage of data filled
            percentage_filled = (filled_fields_count / ((total_fields_count - len(excluded_fields)) * profiles.count())) * 100
            
            return Response({"percentage_filled": round(percentage_filled, 2)})
        else:
#<<<<<<< HEAD
            return Response("User ID not provided", status=status.HTTP_400_BAD_REQUEST) 
#=======
            return Response("User ID not provided", status=status.HTTP_400_BAD_REQUEST)
#>>>>>>> 926376c (server side commite)
