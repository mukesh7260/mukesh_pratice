import json
from django.conf import UserSettingsHolder
from django.http import HttpResponse
from django.shortcuts import render
from httplib2 import Response
import requests
from account.models import User
import datetime
from .models import *
from blogsapi.models import *
from .serializers import ProductSerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from account.models import *
from blogsapi.models import *
# from commentbox.models import *
from otp_reg.models import *
from pagesapi.models import *
from paymentapi.models import *     
from profileapi.models import * 
from rest_framework import generics



import ast

# class ProductView(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
    
#     def get_queryset(self):
#         # Get the 'limit' and 'is_active' parameters from the query parameters
#         limit = self.request.query_params.get('limit', None)
#         is_active = self.request.query_params.get('is_active', None)

#         # Start with the base queryset
#         queryset = Product.objects.all()

#         # Filter by is_active if it's provided as a query parameter
#         if is_active is not None:
#             if is_active.lower() == 'true':
#                 queryset = queryset.filter(is_active=True)
#             elif is_active.lower() == 'false':
#                 queryset = queryset.filter(is_active=False)
#             else:
#                 # Return a bad request response if is_active parameter is not 'true' or 'false'
#                 return Response({'error': 'Invalid value for is_active parameter'}, status=status.HTTP_400_BAD_REQUEST)

#         # Apply the limit if it's a valid positive integer
#         if limit is not None and limit.isdigit() and int(limit) > 0:
#             queryset = queryset.order_by('-id')[:int(limit)]

#         return queryset

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)

from django.utils.dateparse import parse_date

class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        # Get the 'limit', 'is_active', 'start_date', 'end_date', 'user_id', and 'city' parameters from the query parameters
        limit = self.request.query_params.get('limit', None)
        is_active = self.request.query_params.get('is_active', None)
        start_date_str = self.request.query_params.get('start_date', None)
        end_date_str = self.request.query_params.get('end_date', None)
        user_id = self.request.query_params.get('user_id', None)
        city = self.request.query_params.get('city', None)
        business_plan = self.request.query_params.get('business_plan', None)


        # Start with the base queryset
        queryset = Product.objects.all()

        # Filter by is_active if it's provided as a query parameter
        if is_active is not None:
            if is_active.lower() == 'true':
                queryset = queryset.filter(is_active=True)
            elif is_active.lower() == 'false':
                queryset = queryset.filter(is_active=False)
            else:
                # Return a bad request response if is_active parameter is not 'true' or 'false'
                return Response({'error': 'Invalid value for is_active parameter'}, status=status.HTTP_400_BAD_REQUEST)
        if business_plan is not None:
            if business_plan == 'premium':
                queryset = queryset.filter(plan__icontains=business_plan)
            elif business_plan == 'featured':
                queryset = queryset.filter(plan__icontains=business_plan)
            else:
                # Return a bad request response if is_active parameter is not 'true' or 'false'
                return Response({'error': 'Invalid value for business_plan parameter'}, status=status.HTTP_400_BAD_REQUEST)

        # Apply the limit if it's a valid positive integer
        # if limit is not None and limit.isdigit() and int(limit) > 0:
        #     queryset = queryset.order_by('-id')[:int(limit)]

        # Filter by date range if start_date and end_date are provided
        if start_date_str and end_date_str:
            try:
                start_date = parse_date(start_date_str)
                end_date = parse_date(end_date_str)
            except ValueError:
                return Response({'error': 'Invalid date format for start_date or end_date'}, status=status.HTTP_400_BAD_REQUEST)
            
            queryset = queryset.filter(created_date__range=[start_date, end_date])

        # Filter by user ID if provided
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)

        # Filter by city if provided
        if city is not None:
            queryset = queryset.filter(City__icontains=city)
            
        if limit is not None and limit.isdigit() and int(limit) > 0:
            queryset = queryset.order_by('-id')[:int(limit)]

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_serializer(self, *args, **kwargs):
        # Set partial argument based on the HTTP method
        kwargs['partial'] = self.request.method in ['PATCH', 'PUT']
        return super().get_serializer(*args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Deleted successfully"}, status=status.HTTP_200_OK)

# from rest_framework import viewsets
# from rest_framework.pagination import PageNumberPagination

# class ProductPagination(PageNumberPagination):
#     page_size = 1
#     page_size_query_param = 'page_size'
#     max_page_size = 1000

# class ProductView(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     pagination_class = ProductPagination

@api_view(['GET', 'POST'])
def generate_qr_code(request):
    if request.method == 'POST':
        product_id = request.data.get('product_id')

        if not product_id:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Assuming Product model has a method to generate a unique identifier for the QR code
        qr_code_data = Product.objects.get(id=product_id).generate_qr_code_data()

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_code_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        response = HttpResponse(content_type="image/png")
        img.save(response, "PNG")

        return response
    else:
        # If the request method is not POST, you may want to handle it accordingly.
        return Response({'detail': f'Method "{request.method}" not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

#WishList Views
from .models import WishListItems
from rest_framework.generics import CreateAPIView,DestroyAPIView
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from django.shortcuts import get_object_or_404

class AddtoWishListItemsView(CreateAPIView,DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = WishListItems.objects.all()
    serializer_class = WishListItemsTestSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_seller:
            item = get_object_or_404(Product, pk=self.kwargs['pk'])
            serializer.save(owner=user, item=item)
        else:                
            raise serializers.ValidationError("This is not a customer account.Please login as customer.")


    def perform_destroy(self, instance):
        instance.delete()
from django.core import serializers
import ast
class AdsMessageName(APIView):
  def post(self, request, format=None):
    if not request.data.get("adsid"):
        userid=request.data.get("userid")
        UserIdMail=User.objects.get(pk=userid)
        data=adsmangeme.objects.filter(userid=UserIdMail)
        for x in data:
            x.connectMember=x.adsUserId.email
            print("xxxxxxx",x.adsUserId.email)
        qs_json = serializers.serialize('json', data)
        for x in data:
            print(x.message)
            print("dataval;uie",data)
            return HttpResponse(qs_json, content_type='application/json')
    userid=request.data.get("userid")
    UserIdMail=User.objects.get(pk=userid)
    adsid=request.data.get("adsid")
    print("!!!user",UserIdMail.email)
    message=request.data.get("message")
    datetime=request.data.get("datetime")
    adsuserid=Product.objects.get(pk=adsid)
    print("@@@userid",adsuserid.user.id)
    print(request.data.get)
    s=adsmangeme.objects.create(userid=UserIdMail,adsUserId=adsuserid.user,message=message)
    print(s.message)
    s.save()
    # if adsmangeme.objects.filter(userid=userid).filter(adsUserId=adsuserid.user.id):
    #     # updatemessage=adsmangeme.objects.get(userid=userid).get(adsUserId=adsuserid.user.id)
    #     # updatemessage.message[datetime]=message
    #     # updatemessage.save()
    #     updatemessage=adsmangeme.objects.filter(userid=userid).filter(adsUserId=adsuserid.user.id)
    #     for x in updatemessage:
    #         # message={}
    #         # s[datetime]=message
    #         print(x.message)
    #         print(type(x.message))
    #         s=ast.literal_eval(x.message)
    #         print(s)
    #         print(message)
    #         s[datetime]=message
    #         print(s)
    #         x.message=s
    #         x.save()
    #         # print("x",x.message["232/23/2/3"])
    #     print("updatemessage",updatemessage)
    #     # data=json.loads(updatemessage)
    #     print(type(updatemessage))
    #     print("already their ",adsmangeme.objects.filter(userid=userid).get(adsUserId=adsuserid.user.id))
        
    # else:
    #     message={}
    #     message[datetime]=message
    #     s=adsmangeme.objects.create(userid=UserIdMail,adsUserId=adsuserid.user,message=message)
    #     print(s.message)
    #     s.save()
    #     return HttpResponse("stored in database", content_type='application/json')
    #     print("not their ")
    return HttpResponse("qs_json", content_type='application/json')
  def get(self,request):
    userid=request.data.get("userid")
    UserIdMail=User.objects.get(pk=userid)
    
    data=adsmangeme.objects.filter(userid=UserIdMail)
    for x in data:
        x.connectMember=x.adsUserId.email
        print("xxxxxxx",x.adsUserId.email)
    qs_json = serializers.serialize('json', data)
    for x in data:
        print(x.message)
    print("dataval;uie",data)
    return HttpResponse(qs_json, content_type='application/json')


class AdsAdressLatLonView(APIView):
  def get(self, request):
    allads=Product.objects.all()
    for x in allads:
        print("not their ",x.id)
        lat=12.12222
        lon=77.2322
        if(not AdsAdressLatLon.objects.filter(ads=x.id)):
            print("not their ",x.id)
            address=x.locality+x.city+x.state+","+x.zip_code
            print("address value",address)
            # url = "https://address-from-to-latitude-longitude.p.rapidapi.com/geolocationapi"
            # querystring = {"address":address}
            # headers = {
	        #     "X-RapidAPI-Key": "331734c762msh87686d3f66d810fp1c85ebjsn31d2ac2b6d68",
	        #     "X-RapidAPI-Host": "address-from-to-latitude-longitude.p.rapidapi.com"
            # }
            # response = requests.request("GET", url, headers=headers, params=querystring)
            # print("ads latitude longtitude",response.text)
            # print(response.text)
            s=AdsAdressLatLon.objects.create(ads_id=x.id,lat=lat+2,lon=lon+2)
            s.save()
        else:
            print("else block ")
    jsonLatLonData=AdsAdressLatLon.objects.all()
    qs_json = serializers.serialize('json', jsonLatLonData)
    return HttpResponse(qs_json, content_type='application/json')


class chatMessages(APIView):
  def post(self, request, format=None):
    # s=adsmangeme.objects.all().delete()
    userid=request.data.get("userid")
    adsUserEmail=request.data.get("adsUserEmail")
    print("values printing userid adsuseremail",userid,adsUserEmail)
    s=User.objects.get(email=adsUserEmail)
    print("user id ads ",s.pk)
    messageData=adsmangeme.objects.filter(userid=userid,adsUserId=s.pk)
    # for x in messageData:
    #     print(x.message)
    #     print(type(x.message))
        # print( ast.literal_eval(x.message))
        # print(type( ast.literal_eval(x.message)))
        # print(json.dumps(ast.literal_eval(x.message)))
        # data=json.dumps(ast.literal_eval(x.message))
    qs_json = serializers.serialize('json', messageData)
    return HttpResponse(qs_json, content_type='application/json')
# @api_view(['GET', 'POST'])
# def AdsMessage(request):
#     print("@@fjdiojfdoi")
#     if request.method=="POST":
#         print("callking")
#         return render ("stored")

class chatting(APIView):
  def post(self, request, format=None):
    sender=request.data.get("sender")
    reciever=request.data.get("reciever")
    # senderEmailId=User.objects.get(pk=sender)
    # print("senderEmailid",senderEmailId)
    message=request.data.get("message")
    print("fdfjdsl")
    # datetime=str(datetime.datetime.now())
    s=adsmangeme.objects.create(userid=User.objects.get(email=sender),adsUserId=User.objects.get(email=reciever),message=message,connectMember=sender)
    s.save()
    # qs_json = serializers.serialize('json', messageData)
    return HttpResponse("qs_json", content_type='application/json')


class uploadImages(APIView):
    def post(self, request, format=None):
        imagelist=request.data.get("imageList")
        adsid=request.data.get("adsid")
        s=Product.objects.get(pk=adsid)
        print(imagelist)
        # for x in imagelist:
        return HttpResponse("qs_json", content_type='application/json')

class RealEstateEnquery1(APIView):
    def post(self, request, format=None):
        firstName=request.data.get("firstName")
        lastName=request.data.get("lastName")
        email=request.data.get("email")
        zip_code=request.data.get("zip_code")
        s=RealEstateEnquery.objects.create(firstName=firstName,lastName=lastName,email=email,zip_code=zip_code)
        s.save()
        return HttpResponse("sucess", content_type='application/json')


class ReportAds1(APIView):
    def post(self, request, format=None):
        ads=request.data.get("ads")
        adsModel=Product.objects.get(pk=ads)
        reportMessage=request.data.get("report")
        s=ReportAds.objects.create(ads=adsModel,report=reportMessage)
        s.save()
        return HttpResponse("sucess", content_type='application/json')


class AdsUpload(APIView):
    def post(self, request, format=None):
        imageList=request.data.get("imageList")
        adsiD= request.data.get("adsId")
        print(imageList)
        print(adsiD)
        if imageList is None:
            s1= ImageAdsModels.objects.filter(ads_id=adsiD)
            qs_json = serializers.serialize('json', s1)
            return HttpResponse(qs_json, content_type='application/json')
        else:
            s=ImageAdsModels.objects.create(image=imageList,ads_id=adsiD)
            s.save()
            print(s)
            # imageList1=request.data.get("imageList1")
            print("@@@@imagelist data ,ads id",imageList,adsiD)
            print("image view",list(imageList))
        
            return HttpResponse("sucess", content_type='application/json')


class adsCommentBoxView(APIView):
    def post(self, request, format=None):
        ads= request.data.get("ads")
        if "message" not in request.POST:
            print("for data calling ")
            s1=AdsComment.objects.filter(ads_id=ads)
            qs_json = serializers.serialize('json', s1)
            return HttpResponse(qs_json, content_type='application/json')
        email= request.data.get("email")
        message= request.data.get("message")
        rating= request.data.get("rating")
        datevalue= datetime.datetime.now().strftime('%Y-%m-%d')
        print("value")
        s=AdsComment.objects.create(ads_id=ads,email=email,message=message,datetimeValue=datevalue,rating=rating)
        s.save()
        return HttpResponse("Success", content_type='application/json')
    
    def delete(self, request, format=None):
        email_to_delete = request.data.get("email")
        ads_to_delete = request.data.get("ads")
        id = request.data.get("id")

        # Check if the email exists in the comments for the provided ad
        comments_to_delete = AdsComment.objects.filter(email=email_to_delete, ads_id=ads_to_delete, id=id)

        if not comments_to_delete.exists():
            return Response("No comments found for the provided email and ad.", status=status.HTTP_404_NOT_FOUND)

        # Delete the comments associated with the provided email and ad
        comments_to_delete.delete()

        return Response("Comments deleted successfully.", status=status.HTTP_200_OK)

class blogCommentBoxView(APIView):
    def post(self, request, format=None):
        # imageList=request.data.file("imageList")
        blogs= request.data.get("blogs")
        if "message" not in request.POST:
            print("for data calling ")
            s1=BlogComment.objects.filter(ads_id=blogs)
            qs_json = serializers.serialize('json', s1)
            return HttpResponse(qs_json, content_type='application/json')
        email= request.data.get("email")
        message= request.data.get("message")
        datevalue= datetime.datetime.now().strftime('%Y-%m-%d')
        s=BlogComment.objects.create(ads_id=blogs,email=email,message=message,datetimeValue=datevalue)
        s.save()
        # s1=AdsComment.objects.filter(ads=ads)
        # qs_json = serializers.serialize('json', s1)
        return HttpResponse("Success", content_type='application/json')
import qrcode
from PIL import Image

# class qrCodeAds(APIView):
#     def post(self, request, format=None):
#         product= request.data.get("product")
#         Logo_link = 'gfg_QR.png'

#         logo = Image.open(Logo_link)

#         # taking base width
#         basewidth = 100

#         # adjust image size
#         wpercent = (basewidth/float(logo.size[0]))
#         hsize = int((float(logo.size[1])*float(wpercent)))
#         logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
#         QRcode = qrcode.QRCode(
# 	        error_correction=qrcode.constants.ERROR_CORRECT_H
#         )

#         # taking url or text
#         url = 'https://www.geeksforgeeks.org/'

#         # adding URL or text to QRcode
#         QRcode.add_data(url)

#         # generating QR code
#         QRcode.make()

#         # taking color name from user
#         QRcolor = 'black'

#         # adding color to QR code
#         QRimg = QRcode.make_image(
# 	    fill_color=QRcolor, back_color="white").convert('RGB')

#         # set size of QR code
#         pos = ((QRimg.size[0] - logo.size[0]) // 2,
# 	        (QRimg.size[1] - logo.size[1]) // 2)
#         QRimg.paste(logo, pos)

#         # save the QR code generated
#         QRimg.save('gfg_QR.png')
#         return HttpResponse("Success", content_type='application/json')
import qrcode
from PIL import Image
import os
import base64
import hashlib
import secrets

class QrCodeAds(APIView):


  #Ganerating Token Function for product 
  def generate_token(self, product):
        SECRET_KEY = 'secrets.token_urlsafe(32)'
        token_data = f"{product}-{SECRET_KEY}"
        hashed_token = hashlib.sha256(token_data.encode()).hexdigest()
        return hashed_token

  def post(self, request, format=None):

        product= request.data.get("product")
        Logo_link = 'D:/Hola9_main/hola9DjangoLatest/adsapi/hola9.png'
        logo = Image.open(Logo_link)

# taking base width
        basewidth = 100

# adjust image size
        wpercent = (basewidth/float(logo.size[0]))
        hsize = int((float(logo.size[1])*float(wpercent)))

# logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
        logo = logo.resize((basewidth, hsize), Image.LANCZOS)  # Use Image.LANCZOS instead of Image.ANTIALIAS
        QRcode = qrcode.QRCode(
           error_correction=qrcode.constants.ERROR_CORRECT_H)
        
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

        QRimg.save('D:/Hola9_main/hola9DjangoLatest/adsapi/gfg_QR.png')
        logo1 = Image.open("D:/Hola9_main/hola9DjangoLatest/adsapi/gfg_QR.png")
        print(logo1)
        file_path = os.path.join("D:/Hola9_main/hola9DjangoLatest/adsapi/", "gfg_QR.png")
        with open("D:/Hola9_main/hola9DjangoLatest/adsapi/gfg_QR.png", "rb") as image_file:
          encoded_string = base64.b64encode(image_file.read())
        #s=QrCode.objects.create(image=encoded_string,product_id=product)
       
        #token for Product
        token = self.generate_token(product)
        # for saving token in database
        s=QrCode.objects.create(image=encoded_string,product_id=product,token=token)
        
        response_data = {
            'message': 'Success',
            'token': token,
            
        }
        #return HttpResponse("Success", content_type='application/json')
        return JsonResponse(response_data)
class PricingViews(APIView):
    def post(self, request, format=None):
        user=request.data.get("user")
        category =request.data.get("category")
        featured_ads =request.data.get("featured_ads")
        ads_limit =request.data.get("ads_limit")
        ads_timing =request.data.get("ads_timing")
        top_listing=request.data.get("top_listing")
        support=request.data.get("support")
        adsLeft=request.data.get("adsLeft")
        if Pricing.objects.filter(user_id=user):
            s=Pricing.objects.get(user_id=user)
            s.category=category
            s.featured_ads=featured_ads
            s.ads_limit=ads_limit
            s.ads_timing=ads_timing
            s.top_listing=top_listing
            s.support=support
            s.adsLeft=adsLeft
            s.save()
        else:
            s=Pricing.objects.create(user_id=user,category=category,featured_ads=featured_ads,ads_limit=ads_limit,ads_timing=ads_timing,top_listing=top_listing,support=support,adsLeft=adsLeft)
            s.save()
        print("s.id is printing ........................................",s.id)
        return HttpResponse("Success",content_type='application/json') 

class getPricingViews(APIView):
    def post( self,request, format=None):
        user =request.data.get("user")
        s=Pricing.objects.filter(user_id=user)
        print(s)
        data = serializers.serialize('json', s)
        return HttpResponse(data, content_type='application/json')       
class updatePlanLimit(APIView):
    def post( self,request, format=None):
        user =request.data.get("user")
        s=Pricing.objects.filter(user_id=user)
        print(s)
        for x in s:
            x.adsLeft=int(x.adsLeft)-1
            x.adsLeft=str(x.adsLeft)
            x.save()
        return HttpResponse("success", content_type='application/json') 


#under developement userDataCount api
class UserDataCount(APIView):
    def post( self,request, format=None):
        return HttpResponse("success", content_type='application/json')  

# class allAdsByInerval(APIView):
#     def post( self,request, format=None):
#         start =request.data.get("start")
#         end =request.data.get("end")
#         condition=request.data.get("condition")
#         isActive=request.data.get("isActive")
#         user=request.data.get("user")
#         print(type(start),type(end))
#         if isActive:
#             s=Product.objects.filter(is_active=isActive).order_by('-viewsproduct')[int(start):int(end)]
#         else:
#             if condition=="min":
#                 s=Product.objects.filter(is_active=True).filter(expiry=False).filter(deleted=False).order_by('price')[int(start):int(end)]
#             elif  condition =="max":
#                 s=Product.objects.filter(is_active=True).filter(expiry=False).filter(deleted=False).order_by('-price')[int(start):int(end)]
#             elif condition == "featured":
#                 s=Product.objects.filter(is_active=True).filter(expiry=False).filter(deleted=False).filter(~Q(PlanCategory="Free"))[int(start):int(end)]
#             else:
#                 s=Product.objects.filter(is_active=True).filter(expiry=False).filter(deleted=False).order_by('-id')[int(start):int(end)]
#         if user:
#             s=Product.objects.filter(user=user).filter(is_active=True).filter(expiry=False).filter(deleted=False).order_by('-id')[int(start):int(end)]
#         print(s)
#         data = serializers.serialize('json', s)
#         return HttpResponse(data, content_type='application/json') 


# from django.http import JsonResponse
# from django.core import serializers
# from rest_framework.views import APIView
# from rest_framework.response import Response

# class allAdsByInerval(APIView):
#     def post(self, request, format=None):
#         start = request.data.get("start")
#         end = request.data.get("end")
#         limit = request.data.get("limit")

#         try:
#             # Validate and convert input values to integers
#             start = int(start) if start is not None else None
#             end = int(end) if end is not None else None
#             limit = int(limit) if limit is not None else None
#         except ValueError:
#             return JsonResponse({'error': 'Invalid input values'}, status=400)

#         # Initialize the queryset to get all products
#         queryset = Product.objects.all()

#         if start is not None and end is not None:
#             # If both start and end are provided, get the last end-start+1 products
#             count = end - start + 1
#             queryset = queryset.order_by('-id')[start-1:start-1+count]
#         elif limit is not None:
#             # If only limit is provided, get the latest products limited by the specified count
#             queryset = queryset.order_by('-id')[:limit]

#         # Serialize the queryset using Django Rest Framework's Response
#         data = serializers.serialize('json', queryset)
#         return HttpResponse(data, content_type='application/json')

# from django.http import JsonResponse
# from django.core import serializers
# from rest_framework.views import APIView
# from rest_framework.response import Response

# class allAdsByInerval(APIView):
#     def post(self, request, format=None):
#         start = request.data.get("start")
#         end = request.data.get("end")
#         limit = request.data.get("limit")
#         business_plan = request.data.get("businessplan", False)
#         city = request.data.get("City", None)
#         sorting_order = request.data.get("sorting_order", None)

#         try:
#             # Validate and convert input values to integers
#             start = int(start) if start is not None else None
#             end = int(end) if end is not None else None
#             limit = int(limit) if limit is not None else None
#         except ValueError:
#             return JsonResponse({'error': 'Invalid input values'}, status=400)

#         # Initialize the queryset to get all products
#         queryset = Product.objects.all()

#         if business_plan:
#             # If businessplan is True, filter products with plan as "premium" or "featured"
#             queryset = queryset.filter(Q(plan="premium") | Q(plan="featured"))

#         if city:
#             # If City is provided, filter products based on the City field
#             queryset = queryset.filter(City=city)

#         if sorting_order == 'max_to_min':
#             # If max_to_min is provided, sort products by price in descending order
#             queryset = queryset.order_by('-price')
#         elif sorting_order == 'min_to_max':
#             # If min_to_max is provided, sort products by price in ascending order
#             queryset = queryset.order_by('price')

#         if start is not None and end is not None:
#             # If both start and end are provided, get the last end-start+1 products
#             count = end - start + 1
#             queryset = queryset.order_by('-id')[start-1:start-1+count]
#         elif limit is not None:
#             # If only limit is provided, get the latest products limited by the specified count
#             queryset = queryset.order_by('-id')[:limit]

#         # Serialize the queryset using Django Rest Framework's Response
#         data = serializers.serialize('json', queryset)
#         return HttpResponse(data, content_type='application/json')


from django.http import JsonResponse
from django.core import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

class allAdsByInerval(APIView):
    def post(self, request, format=None):
        start = request.data.get("start")
        end = request.data.get("end")
        limit = request.data.get("limit")
        business_plan = request.data.get("businessplan", False)
        city = request.data.get("city", None)
        sorting_order = request.data.get("sorting_order", None)
        search_key = request.data.get("search_key", None)

        try:
            # Validate and convert input values to integers
            start = int(start) if start is not None else None
            end = int(end) if end is not None else None
            limit = int(limit) if limit is not None else None
        except ValueError:
            return JsonResponse({'error': 'Invalid input values'}, status=400)

        # Initialize the queryset to get all products
        queryset = Product.objects.all()

        if business_plan:
            # If businessplan is True, filter products with plan as "premium" or "featured"
            queryset = queryset.filter(Q(plan="premium") | Q(plan="featured"))

        if city:
            # If City is provided, filter products based on the City field
            queryset = queryset.filter(City=city)

        if sorting_order == 'max_to_min':
            # If max_to_min is provided, sort products by price in descending order
            queryset = queryset.order_by('-price')
        elif sorting_order == 'min_to_max':
            # If min_to_max is provided, sort products by price in ascending order
            queryset = queryset.order_by('price')
        elif sorting_order == 'recently':
            # If recently is provided, sort products by id in descending order (latest to old)
            queryset = queryset.order_by('-id')
        elif sorting_order == 'older':
            # If older is provided, sort products by id in ascending order (old to latest)
            queryset = queryset.order_by('id')
        elif sorting_order == 'default':
            # If older is provided, sort products by id in ascending order (old to latest)
            queryset = queryset.order_by('?')
        # if search_key:
        #             # If search_key is provided, dynamically filter based on all fields
        #             search_query = Q()
        #             for field in Product._meta.fields:
        #                 if field.get_internal_type() in ['CharField', 'TextField', 'DecimalField']:
        #                     search_query |= Q(**{f"{field.name}__icontains": search_key})

        #             queryset = queryset.filter(search_query)
        if search_key:
            # If search_key is provided, dynamically filter based on specific fields excluding 'image'
            search_query = Q()
            for field in Product._meta.fields:
                if field.name != 'image' and field.get_internal_type() in ['CharField', 'TextField', 'DecimalField']:
                    search_query |= Q(**{f"{field.name}__icontains": search_key})

            queryset = queryset.filter(search_query)

        if start is not None and end is not None:
            # If both start and end are provided, get the last end-start+1 products
            count = end - start + 1
            queryset = queryset.order_by('-id')[start-1:start-1+count]
        # elif limit is not None:
        #     # If only limit is provided, get the latest products limited by the specified count
        #     queryset = queryset.order_by('-id')[:limit]
        elif limit is not None:
            # If only limit is provided, get the latest products limited by the specified count
            if sorting_order == 'max_to_min':
                queryset = queryset.order_by('-price')[:limit]
            elif sorting_order == 'min_to_max':
                queryset = queryset.order_by('price')[:limit]
            elif sorting_order == 'recently':
                queryset = queryset.order_by('-id')[:limit]
            elif sorting_order == 'older':
                queryset = queryset.order_by('id')[:limit]
            elif sorting_order == 'default':
                queryset = queryset.order_by('?')[:limit]
            else:
                queryset = queryset.order_by('-id')[:limit]

        # Serialize the queryset using Django Rest Framework's Response
        data = serializers.serialize('json', queryset)
        return HttpResponse(data, content_type='application/json')





from django.core import serializers
from django.http import HttpResponse
from rest_framework.views import APIView
from .models import Product

# class categoryAdsByInterval(APIView):
#     def post(self, request, format=None):
#         # start = int(request.data.get("start", 0))
#         # end = int(request.data.get("end", 10))
#         start = request.data.get("start")
#         end = request.data.get("end")
#         limit = request.data.get("limit")
   
#         category = request.data.get("category")
#         subcategory = request.data.get("subCategory")
#         locality = request.data.get("locality")
#         location = request.data.get("location")
#         search_query = request.data.get("searchQuery")
#         min_price = request.data.get("minPrice")
#         max_price = request.data.get("maxPrice")
#         business_plan = request.data.get("businessplan", False)
#         city = request.data.get("city", None)
#         sorting_order = request.data.get("sorting_order", None)
#         search_key = request.data.get("search_key", None)
   
#         try:
#             # Validate and convert input values to integers
#             start = int(start) if start is not None else None
#             end = int(end) if end is not None else None
#             limit = int(limit) if limit is not None else None
#         except ValueError:
#             return JsonResponse({'error': 'Invalid input values'}, status=400)
        

#         queryset = Product.objects.all()
#         if category:
#             queryset = queryset.filter(category=category)

#         if subcategory:
#             queryset = queryset.filter(subCategoryValue=subcategory)

#         if location:
#             queryset = queryset.filter(City=location)

#         if locality and category:
#             queryset = queryset.filter(category=category, locality=locality)

#         if min_price and max_price and search_query:
#             queryset = queryset.filter(
#                 price__gte=int(min_price),
#                 price__lte=int(max_price),
#                 title__icontains=search_query,
#             )
#         if business_plan:
#             # If businessplan is true, filter products with plan set to "premium" or "featured"
#             queryset = queryset.filter(Q(plan="premium") | Q(plan="featured"))
#         if city:
#             # If City is provided, filter products based on the City field
#             queryset = queryset.filter(City=city)
#         if sorting_order == 'max_to_min':
#             # If max_to_min is provided, sort products by price in descending order
#             queryset = queryset.order_by('-price')
#         elif sorting_order == 'min_to_max':
#             # If min_to_max is provided, sort products by price in ascending order
#             queryset = queryset.order_by('price')
#         elif sorting_order == 'recently':
#             # If recently is provided, sort products by id in descending order (latest to old)
#             queryset = queryset.order_by('-id')
#         elif sorting_order == 'older':
#             # If older is provided, sort products by id in ascending order (old to latest)
#             queryset = queryset.order_by('id')
#         elif sorting_order == 'default':
#             # If older is provided, sort products by id in ascending order (old to latest)
#             queryset = queryset.order_by('?')
     


#         if search_key:
#             # If search_key is provided, dynamically filter based on specific fields excluding 'image'
#             search_query = Q()
#             for field in Product._meta.fields:
#                 if field.name != 'image' and field.get_internal_type() in ['CharField', 'TextField', 'DecimalField']:
#                     search_query |= Q(**{f"{field.name}__icontains": search_key})

#             queryset = queryset.filter(search_query)
#         # queryset = queryset.filter(is_active=True, expiry=False, deleted=False)[start:end]
#         # if start is not None and end is not None:
#         #     # If both start and end are provided, get the last end-start+1 products
#         #     count = end - start + 1
#         #     # queryset = queryset.order_by('-id')[start-1:start-1+count]
#         #     queryset = queryset.order_by('-id')[start:start+count]
#         if start is not None and end is not None:
#             # If both start and end are provided, get the last end-start+1 products
#             count = end - start + 1
#             queryset = queryset.order_by('-id')[start-1:start-1+count]
#         elif limit is not None:
#             # If only limit is provided, get the latest products limited by the specified count
#             if sorting_order == 'max_to_min':
#                 queryset = queryset.order_by('-price')[:limit]
#             elif sorting_order == 'min_to_max':
#                 queryset = queryset.order_by('price')[:limit]
#             elif sorting_order == 'recently':
#                 queryset = queryset.order_by('-id')[:limit]
#             elif sorting_order == 'older':
#                 queryset = queryset.order_by('id')[:limit]
#             elif sorting_order == 'default':
#                 queryset = queryset.order_by('?')[:limit]
#             else:
#                 queryset = queryset.order_by('-id')[:limit]
            


#         data = serializers.serialize("json", queryset)
#         return HttpResponse(data, content_type="application/json")

# **************************************************************************


class categoryAdsByInterval(APIView):
    def post(self, request, format=None):
        # start = int(request.data.get("start", 0))
        # end = int(request.data.get("end", 10))
        start = request.data.get("start")
        end = request.data.get("end")
        limit = request.data.get("limit")
   
        category = request.data.get("category")
        subcategory = request.data.get("subCategory")
        locality = request.data.get("locality")
        location = request.data.get("location")
        search_query = request.data.get("searchQuery")
        min_price = request.data.get("minPrice")
        max_price = request.data.get("maxPrice")
        business_plan = request.data.get("businessplan", False)
        city = request.data.get("city", None)
        sorting_order = request.data.get("sorting_order", None)
        search_key = request.data.get("search_key", None)
   
        try:
            # Validate and convert input values to integers
            start = int(start) if start is not None else None
            end = int(end) if end is not None else None
            limit = int(limit) if limit is not None else None
        except ValueError:
            return JsonResponse({'error': 'Invalid input values'}, status=400)
        

        queryset = Product.objects.all()
        if category:
            queryset = queryset.filter(category=category)

        if subcategory:
            queryset = queryset.filter(subCategoryValue=subcategory)

        if location:
            queryset = queryset.filter(City=location)

        if locality and category:
            queryset = queryset.filter(category=category, locality=locality)

        if min_price and max_price and search_query:
            queryset = queryset.filter(
                price__gte=int(min_price),
                price__lte=int(max_price),
                title__icontains=search_query,
            )
        if business_plan:
            # If businessplan is true, filter products with plan set to "premium" or "featured"
            queryset = queryset.filter(Q(plan="premium") | Q(plan="featured"))
        if city:
            # If City is provided, filter products based on the City field
            queryset = queryset.filter(City=city)
        if sorting_order == 'max_to_min':
            # If max_to_min is provided, sort products by price in descending order
            queryset = queryset.order_by('-price')
        elif sorting_order == 'min_to_max':
            # If min_to_max is provided, sort products by price in ascending order
            queryset = queryset.order_by('price')
        elif sorting_order == 'recently':
            # If recently is provided, sort products by id in descending order (latest to old)
            queryset = queryset.order_by('-id')
        elif sorting_order == 'older':
            # If older is provided, sort products by id in ascending order (old to latest)
            queryset = queryset.order_by('id')
        elif sorting_order == 'default':
            # If older is provided, sort products by id in ascending order (old to latest)
            queryset = queryset.order_by('?')
     


        if search_key:
            # If search_key is provided, dynamically filter based on specific fields excluding 'image'
            search_query = Q()
            for field in Product._meta.fields:
                if field.name != 'image' and field.get_internal_type() in ['CharField', 'TextField', 'DecimalField']:
                    search_query |= Q(**{f"{field.name}__icontains": search_key})

            queryset = queryset.filter(search_query)
        # queryset = queryset.filter(is_active=True, expiry=False, deleted=False)[start:end]
        # if start is not None and end is not None:
        #     # If both start and end are provided, get the last end-start+1 products
        #     count = end - start + 1
        #     # queryset = queryset.order_by('-id')[start-1:start-1+count]
        #     queryset = queryset.order_by('-id')[start:start+count]
        total_length = queryset.count()

        if start is not None and end is not None:
            # If both start and end are provided, get the last end-start+1 products
            count = end - start + 1
            queryset = queryset.order_by('-id')[start-1:start-1+count]
        elif limit is not None:
            # If only limit is provided, get the latest products limited by the specified count
            if sorting_order == 'max_to_min':
                queryset = queryset.order_by('-price')[:limit]
            elif sorting_order == 'min_to_max':
                queryset = queryset.order_by('price')[:limit]
            elif sorting_order == 'recently':
                queryset = queryset.order_by('-id')[:limit]
            elif sorting_order == 'older':
                queryset = queryset.order_by('id')[:limit]
            elif sorting_order == 'default':
                queryset = queryset.order_by('?')[:limit]
            else:
                queryset = queryset.order_by('-id')[:limit]
                
        response_data = [
            {'model': 'adsapi.product', 'pk': item.pk, 'fields': serializers.serialize('python', [item])[0]['fields']}
            for item in queryset
        ]

        # Prepend the 'length' field to the list
        # response_data.insert(0, {'length': len(response_data)})
        response_data = [{'length': total_length}] + response_data



        return JsonResponse(response_data, safe=False)           


        # data = serializers.serialize("json", response_data)
        # return HttpResponse(data, content_type="application/json",safe=False)
# **************************************************************************************
    
class subCategoryAdsByInterva(APIView):
    def post( self,request, format=None):
        start =request.data.get("start")
        end =request.data.get("end")
        subCategory=request.data.get("subCategory")
        s=Product.objects.filter(subCategoryValue=subCategory)[int(start):int(end)]
        print(s)
        data = serializers.serialize('json', s)
        return HttpResponse(data, content_type='application/json')  
class adminAuth(APIView):
    def post( self,request, format=None):
        username =request.data.get("username")
        password=request.data.get("password")
        s=AdminAuth.objects.filter(username=username).filter(password=password)
        if s:
            return HttpResponse("true", content_type='application/json')
        else:
            return HttpResponse("false", content_type='application/json')  


class webCountData(APIView):
    def post( self,request, format=None):
        dateads = request.data.get("dateads")
        if dateads=="all":
                data={"user":{
                "Register":[User.objects.all().count()],
                "temetrydaa":[TelemetryDaa.objects.all().count()],
                "ReviewSection":[ReviewSection.objects.all().count()],
                "jobs":[JobApply.objects.all().count()],
                "jobsrequired":[JobsRequired.objects.all().count()]
            },
            "ads":{
                "ads":[Product.objects.all().count()],
                "premium":[Pricing.objects.all().count()],
                "payment_detail":[PaymentDetailsValues.objects.all().count()],
                "RealEstateEnquery":[RealEstateEnquery.objects.all().count()],
                "AdminAuth":[AdminAuth.objects.all().count()],
                "adsmangeme":[adsmangeme.objects.all().count()],
                "LastLogin":[LastLogin.objects.all().count()],
                "ReportAds":[ReportAds.objects.all().count()]
            },
            "Payment":{
                "Order":[Order.objects.all().count()],
                "TransationIdone":[TransationIdone.objects.all().count()]
            },
            "OTP_registration":{
                "OTPVerifiaction":[OTPVerifiaction.objects.all().count()]
            },
            "Blogs":{
                "Blogs":[Blogs.objects.all().count()],
                "BlogComment":[BlogComment.objects.all().count()]
            },
            "Comentbox":{
                "AdsComment":[AdsComment.objects.all().count()]
            },
            "Contact":{
                "contacts":[Contact.objects.all().count()]
            },
            "Profile":{
                "Profile":[Profile.objects.all().count()]
            }
            }
        else:
            data={"user":{
            # "Register":User.objects.filter(created_at=dateads).count(),
            "RegisterData":User.objects.filter(created_at=dateads).count(),
            "telemetrydaa":TelemetryDaa.objects.filter(date=dateads).count(),
            "ReviewSection":ReviewSection.objects.filter(created_at=dateads).count(),
            "jobs":JobApply.objects.filter(created_at=dateads).count(),
            "jobsrequired":JobsRequired.objects.filter(created_at=dateads).count(),


        },
        "ads":{
            "ads":Product.objects.filter(date_created=dateads).count(),
            "premium_ads":Product.objects.filter(~Q(PlanCategory="Free")).filter(date_created=dateads).count(),
            "premium_plan":Pricing.objects.filter(ads_timing=dateads).count(),
            "payment_detail":PaymentDetailsValues.objects.filter(date=dateads).count(),
            # "AdsComment":AdsComment.objects.filter(datetimeValue=dateads).count(),
            "RealEstateEnquery":RealEstateEnquery.objects.filter(date_created=dateads).count(),
        },
        "Payment":{
            "Order":Order.objects.filter(order_dateTele=dateads).count(),
            "TransationIdone":TransationIdone.objects.filter(date_created=dateads).count(),
        },
        # "OTP_registration":{
        #     "OTPVerifiaction":OTPVerifiaction.objects.filter(date=dateads).count(),
        # },
        "Blogs":{
            "Blogs":Blogs.objects.filter(published_time=dateads).count(),
            "BlogComment":BlogComment.objects.filter(datetimeValue=dateads).count(),
        },
        "Comentbox":{
            # "AdsComment":AdsComment.objects.filter(date=dateads).count(),
        },
        "Contact":{
            "contacts":Contact.objects.filter(created_at=dateads).count(),
        },
        "Profile":{
            "Profile":Profile.objects.filter(date=dateads).count(),
        }
        }

        return HttpResponse(json.dumps(data) , content_type='application/json')  

    

class featuredAdsData(APIView):
    def post( self,request, format=None):
        start =request.data.get("start")
        end =request.data.get("end")
        category=request.data.get("category")
        if category :
            ads=Product.objects.filter(category=category)
        else:
            ads=Product.objects.all()
        recommended=ads.filter(plan="Gold").filter(is_active=True).filter(expiry=False).filter(deleted=False)
        Premium=ads.filter(plan="Platinum").filter(is_active=True).filter(expiry=False).filter(deleted=False)
        Featured=ads.filter(plan="Silver").filter(is_active=True).filter(expiry=False).filter(deleted=False)
        s=recommended.union(Premium,Featured).reverse()
        s1 = serializers.serialize('json', s[int(start):int(end)])
        return HttpResponse(s1 , content_type='application/json') 
class webCountAsperDate (APIView):
    def post( self,request , format=None):
        dateads = request.data.get("dateads")
        ads=Product.objects.filter(date_created=dateads).count()
        premium=Pricing.objects.filter(ads_timing=dateads).count()
        user=User.objects.filter(created_at=dateads).count()
        blog=Blogs.objects.filter(published_time=dateads).count()
        premium=Pricing.objects.filter(ads_timing=dateads).count()
        data={"ads":ads,"user":user,"blog":blog,"premium":premium}
        return HttpResponse(json.dumps(data), content_type='application/json')    
        

class webCountasPerDateData(APIView) :
    def post( self,request , format=None): 
        dateads = request.data.get("dateads")
        if dateads=="all":
            s=Product.objects.all()
        else:
            # s = Product.objects.filter(created_date=dateads)
            s = Product.objects.filter(created_date__date=dateads)

            # s=Product.objects.filter(date_created=dateads)
        data = serializers.serialize('json', s) 
        return HttpResponse(data, content_type='application/json') 



class webCountUSERPerDateData(APIView) :
    def post( self,request, format=None): 
        dateads = request.data.get("dateads")
        print(type(dateads))
        finalData={}
        # print(dateads)
        if dateads=="all":
            finalData["RegisterData"]= serializers.serialize('json', User.objects.all()),
            finalData["TelemetryDaa"]= serializers.serialize('json',TelemetryDaa.objects.all()),
            finalData["ReviewSection"]= serializers.serialize('json',ReviewSection.objects.all()),
            finalData["Jobs"]= serializers.serialize('json',JobApply.objects.all()),
            finalData["jobsrequired"]= serializers.serialize('json',JobsRequired.objects.all())
            finalData["ads"]= serializers.serialize('json',Product.objects.all()),
            finalData["premium"]= serializers.serialize('json',Pricing.objects.all()),
            finalData["payment_details"]= serializers.serialize('json',PaymentDetailsValues.objects.all()),
            finalData["RealEstateEnquery"]= serializers.serialize('json',RealEstateEnquery.objects.all()),
            finalData["Blogs"]=serializers.serialize('json',Blogs.objects.all()),
            finalData["Blogscomment"]=serializers.serialize('json',BlogComment.objects.all()),
            finalData["AdsComment"]=serializers.serialize('json',AdsComment.objects.all()),
            finalData["Contact"]=serializers.serialize('json',Contact.objects.all()),
            finalData["Profile"]=serializers.serialize('json',Profile.objects.all()),
            finalData["Order"]=serializers.serialize('json',Order.objects.all()),
            finalData["TransationIdone"]=serializers.serialize('json',TransationIdone.objects.all()),
            finalData["OTPVerifiaction"]=serializers.serialize('json',OTPVerifiaction.objects.all()),
            finalData["AdminAuth"]=serializers.serialize('json',AdminAuth.objects.all()),
            finalData["adsmangeme"]=serializers.serialize('json',adsmangeme.objects.all()),
            finalData["LastLogin"]=serializers.serialize('json',LastLogin.objects.all()),
            finalData["ReportAds"]=serializers.serialize('json',ReportAds.objects.all())

        else: 

            finalData["RegisterData"]=serializers.serialize('json',User.objects.filter(created_at=dateads))
            finalData["telemetrydaa"]=serializers.serialize('json',TelemetryDaa.objects.filter(date=dateads))
            finalData["ReviewSection"]=serializers.serialize('json',ReviewSection.objects.filter(created_at=dateads))
            finalData["jobs"]=serializers.serialize('json',JobApply.objects.filter(created_at=dateads))
            finalData["jobsrequired"]=serializers.serialize('json',JobsRequired.objects.filter(created_at=dateads))
            finalData["ads"]=serializers.serialize('json',Product.objects.filter(date_created=dateads))
            finalData["premium"]=serializers.serialize('json',Pricing.objects.filter(ads_timing=dateads))
            finalData["payment_detail"]=serializers.serialize('json',PaymentDetailsValues.objects.filter(date=dateads))
            finalData["RealEstateEnquery"]=serializers.serialize('json',RealEstateEnquery.objects.filter(date_created=dateads))
            finalData["Blogs"]=serializers.serialize('json',Blogs.objects.filter(published_time=dateads))
            finalData["BlogComment"]=serializers.serialize('json',BlogComment.objects.filter(datetimeValue=dateads))
            finalData["AdsComment"]=serializers.serialize('json',AdsComment.objects.filter(date=dateads))
            finalData["contacts"]=serializers.serialize('json',Contact.objects.filter(created_at=dateads))
            finalData["Profile"]=serializers.serialize('json',Profile.objects.filter(date=dateads))
            finalData["Order"]=serializers.serialize('json',Order.objects.filter(order_dateTele=dateads))
            finalData["OTPVerifiaction"]=serializers.serialize('json',OTPVerifiaction.objects.filter(date=dateads))
            finalData["TransationIdone"]=serializers.serialize('json',TransationIdone.objects.filter(date_created=dateads))
            # finalData["AdminAuth"]=serializers.serialize('json',AdminAuth.objects.filter(date=dateads))
            finalData["adsmangeme"]=serializers.serialize('json',adsmangeme.objects.filter(date_created=dateads))
            # finalData["LastLogin"]=serializers.serialize('json',LastLogin.objects.filter(date=dateads))
            finalData["ReportAds"]=serializers.serialize('json',ReportAds.objects.filter(dates=dateads))          
        return HttpResponse(json.dumps(finalData),content_type='application/json')

class webCountBLOGSPerDateData(APIView) :
    def post( self,request , format=None): 
        dateads = request.data.get("dateads") 
        if dateads=="all":
            s=Blogs.objects.all()
        else: 
            s=Blogs.objects.filter(published_time=dateads)
        data = serializers.serialize('json', s) 
        return HttpResponse(data, content_type='application/json') 

import pandas
from datetime import timedelta
from datetime import datetime
class dataCuntMultipleValues(APIView) :
    def post( self,request , format=None): 
        data={"index":[],"value":[]}
        requestData=request.data.get("requestData")
        start = request.data.get("start") 
        start = datetime.datetime.strptime(start[2:], '%y-%m-%d')
        end = request.data.get("end") 
        end = datetime.datetime.strptime(end[2:], '%y-%m-%d')
        print(start>end,start.strftime('%Y-%m-%d'),end.strftime('%Y-%m-%d'))
        alldates=[]
        print(end,start)
        delta = end-start
        for i in range(delta.days + 1):
            day = start + timedelta(days=i)
            print("daym",type(day.strftime('%Y-%m-%d')))
            if(requestData=="user"):
                s=User.objects.filter(created_at=day.strftime('%Y-%m-%d')).count()
            elif(requestData=="ads"):
                s=Product.objects.filter(date_created=day.strftime('%Y-%m-%d')).count()
            elif(requestData=="blog"):
                s=Blogs.objects.filter(published_time=day.strftime('%Y-%m-%d')).count()
            data["index"].append(day.strftime('%Y-%m-%d'))
            data["value"].append(s)
        print(data)
        return HttpResponse(json.dumps(data), content_type='application/json')
    
    
    
# import ast
# import difflib
# class AdsDataFilter(APIView) :
#     def post( self,request , format=None):
#         start =request.data.get("start")
#         end= request.data.get("end")
#         print("hi")
#         # requestData=ast.literal_eval(request.data.get("requestData"))
#         requestData = request.data.get("requestData")
#         print("hello")
#         extraField=requestData["extrafiled"] if type(requestData["extrafiled"]) is dict   else ast.literal_eval(requestData["extrafiled"])
#         del requestData['extrafiled']
#         print(requestData,extraField)
#         s=Product.objects.all()
#         print(s.count()) 
#         filters = {}
#         for key1 in requestData:
#             if not (key1=="minPrice" or key1=="maxPrice" or key1=="searchValue"):
#                 key1=key1
#                 filters[key1] = requestData[key1]
#         s1=Product.objects.filter(**filters)
#         print(Product.objects.filter(subCategoryValue="Refrigerators/Fridge").filter(category="Furniture"))
#         print(s1)
#         if 'minPrice' in requestData or 'maxPrice' in requestData:
#             print("pricing---------")
#             s1=s1.filter(price__gte=int(requestData['minPrice']),price__lte=int(requestData['maxPrice']))
#             print("pricing",s1)
#         finalProduct=Product.objects.filter(category="e3322222")
#         # ////
        
#         # print("latest",finalProduct)
#         # if 'City' in requestData:
#         #     city_value = requestData['City']
#         #     s1 = s1.filter(City__icontains=city_value)
            
#         # /////
#         # finalProduct=Product.objects.filter(category="e3322222")
#         finalProduct = Product.objects.none()

#         if len(extraField) != 0:
#             aa={}
#             for x in extraField:
#                 z1=x.encode("ascii", "ignore")
#                 z2=extraField[x].encode("ascii", "ignore")
#                 z11=z1.decode()
#                 z44=z2.decode()
#                 aa[z11]=z44
#             extraField=aa
#             print("extraField",extraField,type(extraField))
#             for x1 in s1:
#                 count=len(extraField)
#                 countTemp=0
#                 if x1.extraField:
#                     if (not x1.extraField =="null"):
#                         x1.extraField=ast.literal_eval(x1.extraField)
#                         newTempObjProdctExtraFiled={}
#                         for x in x1.extraField:
#                             z1=x.encode("ascii", "ignore")
#                             # print(x1.extraField[x].encode("ascii", "ignore"))
#                             # print("---------------",x1.extraField[x])
#                             if type(x1.extraField[x])==list:
#                                 x1.extraField[x]=x1.extraField[x][0]
#                             if type(x1.extraField[x])==int:
#                                 print("interger value")
#                                 x1.extraField[x]=str(x1.extraField[x])
#                             print("-----fdddddddddddd",x1.extraField[x])
#                             z2=x1.extraField[x].encode("ascii", "ignore")
#                             z11=z1.decode()
#                             z44=z2.decode()
#                             newTempObjProdctExtraFiled[z11]=z44
#                         print("000000",newTempObjProdctExtraFiled)
#                         for singlekeyValue in extraField:
#                             print("that is the something",singlekeyValue,newTempObjProdctExtraFiled.keys())
                            
#                             if singlekeyValue in newTempObjProdctExtraFiled.keys():
#                                 print("extra one")
#                                 m=difflib.SequenceMatcher(None,extraField[singlekeyValue],newTempObjProdctExtraFiled[singlekeyValue]).ratio()
#                                 print(",,,,,,,,,,,,,,,,,,,,,,,,",extraField[singlekeyValue],newTempObjProdctExtraFiled[singlekeyValue],m)
#                                 if(m*100>50):
#                                     countTemp=countTemp+1
#                             # if extraField[singlekeyValue] is newTempObjProdctExtraFiled[singlekeyValue]:
#                             #     countTemp=countTemp+1
#                             #     print("checking")
#                 print(count,countTemp,x1.pk)
#                 print(type(count),type(countTemp))
#                 if(count==countTemp):
#                     t1=Product.objects.filter(pk=x1.pk).filter(is_active=True).filter(expiry=False).filter(deleted=False)
#                     if t1 :
#                         finalProduct=finalProduct.union(t1)
#         if "tital" in requestData:
#             print("tital is also calling",requestData["title"])
#             s1=s1.filter(title__icontains=requestData["title"])
#             finalProduct=finalProduct.filter(title__icontains=requestData["title"])
#         print("data in tital",s1.count())
#         finalProduct = serializers.serialize('json', finalProduct[int(start):int(end)] if len(extraField) != 0 else s1.filter(is_active=True).filter(expiry=False).filter(deleted=False)[int(start):int(end)]) 
#         return HttpResponse(finalProduct, content_type='application/json')  
        

# ****************************************************************************** Updated One
# import ast
# from django.http import HttpResponse
# from rest_framework.views import APIView
# from .models import Product

# class AdsDataFilter(APIView):
#     def post(self, request, format=None):
#         try:
#             start = int(request.data.get("start", 0))
#             end = int(request.data.get("end", 10))
#             requestData = request.data.get("requestData", {})
#         except ValueError:
#             return HttpResponse("Invalid data format.", status=400)

#         extraField = requestData.get("extraField", {})
#         minPrice = requestData.get("minPrice")
#         maxPrice = requestData.get("maxPrice")

#         filters = {}

#         # Apply filters based on requestData
#         for key, value in requestData.items():
#             if key not in ["extraField", "minPrice", "maxPrice"]:
#                 filters[key] = value
        
#         # Apply filters to the Product queryset
#         products = Product.objects.filter(**filters)
        
#         if minPrice is not None and maxPrice is not None:
#             products = products.filter(price__gte=minPrice, price__lte=maxPrice)
        
#         final_products = []

#         # Apply extra field filtering
#         if extraField:
#             for product in products:
#                 extra_field_data = product.extraField
#                 if extra_field_data:
#                     try:
#                         extra_field_data = ast.literal_eval(extra_field_data)
#                     except (SyntaxError, ValueError):
#                         extra_field_data = {}

#                     match_all_fields = all(
#                         extraField.get(field_key) == extra_field_data.get(field_key)
#                         for field_key in extraField
#                     )
                    
#                     if match_all_fields:
#                         final_products.append(product)

#         if not final_products:
#             final_products = products
        
#         serialized_products = serializers.serialize('json', final_products[start:end])
#         return HttpResponse(serialized_products, content_type='application/json')

# ***************************************************************************
# import ast
# from django.http import HttpResponse
# from rest_framework.views import APIView
# from .models import Product

# class AdsDataFilter(APIView):
#     def post(self, request, format=None):
#         try:
#             start = int(request.data.get("start", 0))
#             end = int(request.data.get("end", 10))
#             requestData = request.data.get("requestData", {})
#         except ValueError:
#             return HttpResponse("Invalid data format.", status=400)

#         extraField = requestData.get("extraField", {})
#         minPrice = requestData.get("minPrice")
#         maxPrice = requestData.get("maxPrice")
#         category = requestData.get("category")
#         city = requestData.get("City")

#         filters = {}

#         # Apply filters based on requestData
#         for key, value in requestData.items():
#             if key not in ["extraField", "minPrice", "maxPrice", "category", "City"]:
#                 filters[key] = value
        
#         # Apply filters to the Product queryset
#         products = Product.objects.filter(**filters)
        
#         if minPrice is not None and maxPrice is not None:
#             products = products.filter(price__gte=minPrice, price__lte=maxPrice)
        
#         final_products = []

#         # Apply extra field filtering
#         if extraField:
#             for product in products:
#                 extra_field_data = product.extraField
#                 if extra_field_data:
#                     try:
#                         extra_field_data = ast.literal_eval(extra_field_data)
#                     except (SyntaxError, ValueError):
#                         extra_field_data = {}

#                     match_all_fields = all(
#                         extraField.get(field_key) == extra_field_data.get(field_key)
#                         for field_key in extraField
#                     )
                    
#                     if match_all_fields:
#                         final_products.append(product)

#         if not final_products:
#             final_products = products
        
#         # Apply category and city filtering
#         if category:
#             final_products = [product for product in final_products if product.category == category]
#         if city:
#             final_products = [product for product in final_products if product.City == city]
        
#         serialized_products = serializers.serialize('json', final_products[start:end])
#         return HttpResponse(serialized_products, content_type='application/json')




import ast
from django.http import HttpResponse
from rest_framework.views import APIView
from .models import Product

class AdsDataFilter(APIView):
    def post(self, request, format=None):
        try:
            start = int(request.data.get("start", 0))
            end = int(request.data.get("end", 10))
            requestData = request.data.get("requestData", {})
        except ValueError:
            return HttpResponse("Invalid data format.", status=400)

        extraField = requestData.get("extraField", {})
        minPrice = requestData.get("minPrice")
        maxPrice = requestData.get("maxPrice")
        category = requestData.get("category")
        city = requestData.get("City")

        filters = {}

        # Apply filters based on requestData
        for key, value in requestData.items():
            if key not in ["extraField", "minPrice", "maxPrice", "category", "City"]:
                filters[key] = value
        
        # Apply filters to the Product queryset
        products = Product.objects.filter(**filters)
        
        if minPrice is not None and maxPrice is not None:
            products = products.filter(price__gte=minPrice, price__lte=maxPrice)
        
        final_products = []

        # Apply extra field filtering
        if extraField:
            for product in products:
                extra_field_data = product.extraField
                if extra_field_data:
                    try:
                        extra_field_data = ast.literal_eval(extra_field_data)
                    except (SyntaxError, ValueError):
                        extra_field_data = {}

                    match_all_fields = all(
                        extraField.get(field_key) == extra_field_data.get(field_key)
                        for field_key in extraField
                    )
                    
                    if match_all_fields:
                        final_products.append(product)

        if not final_products:
            final_products = products
        
        # Apply City filtering
        if city:
            final_products = [product for product in final_products if product.City == city]
        
        # Apply category filtering if provided
        if category:
            final_products = [product for product in final_products if product.category == category]
        
        serialized_products = serializers.serialize('json', final_products[start:end])
        return HttpResponse(serialized_products, content_type='application/json')


    
# Creates a sorted dictionary (sorted by key)
from collections import OrderedDict
class allPlanData(APIView):
    def post( self,request , format=None):
        userId=request.data.get("user")
        # print(Product.objects.filter(user_id=46))
        # print(user)
        # obj={}
        # obj["Free"]=Product.objects.filter(user=user).filter(PlanCategory="Free").count()
        # print(obj)
        # obj1={}
        # obj1["Premium"]=Product.objects.filter(user=user).filter(PlanCategory="Premium").count()
        # print(obj1)
        # obj2={}
        # obj2["Recommended"]=Product.objects.filter(user=user).filter(PlanCategory="Recommended").count()
        # print(obj2)
        # obj3={}
        # obj3["Featured"]=Product.objects.filter(user=user).filter(PlanCategory="Featured").count()
        # print(obj3)
        # result = json.dumps(obj)
        # result1 = json.dumps(obj1)
        # result2=json.dumps(obj2)
        # result3=json.dumps(obj3)
        allPricingPlanData=Pricing.objects.filter(user=userId)
        planObj={"free":0,"premium":0,"featured":0,"recommended":0}
        allPricingPlanDataList=[]
        for x in allPricingPlanData:
            if(x.category=="Free"):
                planObj["free"]=(planObj["free"]+1)
            elif (x.category=="Featured"):
                planObj["featured"]=(planObj["featured"]+1)
            elif (x.category=="Premium"):
                planObj["premium"]=(planObj["premium"]+1)
            elif (x.category=="Recommended"):
                planObj["recommended"]=(planObj["recommended"]+1)
            allPricingPlanDataList.append(x.category)
        
        planObj["free"]=planObj["free"]*5
        planObj["premium"]=planObj["premium"]*60
        planObj["featured"]=planObj["featured"]*20
        planObj["recommended"]=planObj["recommended"]*100
        print(allPricingPlanDataList)
        print(planObj)
        currentUserPlan=Pricing.objects.filter(user=userId).order_by('-id')[:1]
        currentUserPlanCategory=None
        for x in currentUserPlan:
            currentUserPlanCategory=x.category
        print(currentUserPlan)
        totalUserAds=Product.objects.filter(user=userId)
        finalObj={"totalCount":{
                    "free":[Product.objects.filter(user=userId).filter(PlanCategory="Free").count(),planObj["free"]-Product.objects.filter(user=userId).filter(PlanCategory="Free").count()],
                    "featured":[Product.objects.filter(user=userId).filter(PlanCategory="Featured").count(),planObj["featured"]-Product.objects.filter(user=userId).filter(PlanCategory="Featured").count()],
                    "premium":[Product.objects.filter(user=userId).filter(PlanCategory="Premium").count(),planObj["premium"]-Product.objects.filter(user=userId).filter(PlanCategory="Premium").count()],
                    "recommended":[Product.objects.filter(user=userId).filter(PlanCategory="Recommended").count(),planObj["recommended"]-Product.objects.filter(user=userId).filter(PlanCategory="Recommended").count()]}
                    ,"currentPlan":currentUserPlanCategory,"TotalPlan":list(set(allPricingPlanDataList)),"leftPlan":[]}
        print(finalObj)
        if(not finalObj["totalCount"]["free"][1]==0):
            finalObj["leftPlan"].append("Free")
        if(not finalObj["totalCount"]["featured"][1]==0):
            finalObj["leftPlan"].append("Featured")
        if(not finalObj["totalCount"]["premium"][1]==0):
            finalObj["leftPlan"].append("Premium")
        if(not finalObj["totalCount"]["recommended"][1]==0):
            finalObj["leftPlan"].append("Recommended")
        print(finalObj)
        
        templist=[]
        for key in finalObj["totalCount"]:
            if(finalObj["totalCount"][key][0]==0 and finalObj["totalCount"][key][1]==0):
                templist.append(key)
        temoObj=finalObj["totalCount"]
        for i in templist:
            temoObj.pop(i)
            print(temoObj)
        finalObj["totalCount"]=temoObj
        # finalObj["totalCount"]= OrderedDict(sorted(finalObj["totalCount"].items()))
        result2=json.dumps(finalObj)
        # nalProduct = serializers.serialize('json',result) 
        return HttpResponse(result2, content_type='application/json')


class wishlistData(APIView):
    def post( self,request , format=None):
        condition=request.data.get("request")
        wishlist=request.data.get("wishlist")
        print("wihlist list data ",wishlist,type(wishlist))
        user=request.data.get('user')
        if condition =="GET":
            print("hello")
            finalWishlist=WishlistData.objects.filter(User_id=user)
            finalProduct = serializers.serialize('json', finalWishlist) 
            if not WishlistData.objects.filter(User_id=user):
                finalProduct = serializers.serialize('json', []) 
            return HttpResponse(finalProduct, content_type='application/json')
        if WishlistData.objects.filter(User_id=user):
            s=WishlistData.objects.get(User_id=user)
            s.wishlistData=wishlist
            s.save()
        else:
            s1=WishlistData.objects.create(wishlistData=wishlist,User_id=user)
            s1.save()
        finalWishlist=WishlistData.objects.filter(User_id=user)
        finalProduct = serializers.serialize('json', finalWishlist) 
        return HttpResponse(finalProduct, content_type='application/json')
    def get(self,request):
        user=request.data.get('user')
        finalWishlist=WishlistData.objects.filter(User_id=user)
        finalProduct = serializers.serialize('json', finalWishlist) 
        return HttpResponse(finalProduct, content_type='application/json')


class allPricingPlanData(APIView):
    def post( self,request , format=None):
        userId=request.data.get("user")
        allPricingPlanData=Pricing.objects.filter(user=userId)
        s=Product.objects.filter(user=userId)
        for x in s:
            print(x.plan)
        print("@@@@@@@sss value",s)
        totalPlans=[]
        planObj={"free":0,"Silver":0,"Gold":0,"Platinum":0}
        for x in allPricingPlanData:
            if(x.category=="Free"):
                planObj["free"]=planObj["free"]+1
            elif(x.category=="Silver"):
                planObj["Silver"]=planObj["Silver"]+1
            elif(x.category=="Gold"):
                planObj["Gold"]=planObj["Gold"]+1
            elif(x.category=="Platinum"):
                planObj["Platinum"]=planObj["Platinum"]+1
            totalPlans.append(x.category)
        finalObj={"planDataDetails":{},"postAdsForm":{},"leftPlan":[]}
        finalObj["totalPlan"]=[*set(totalPlans)]
        finalObj["numberOfTimePlan"]=planObj
        for plan in finalObj["totalPlan"]:
            if plan=="Free":
                finalObj["planDataDetails"]["Free"]={}
                finalObj["planDataDetails"]["Free"]["totalAds"]=3
                finalObj["planDataDetails"]["Free"]["reponse"]="Limited"
                finalObj["planDataDetails"]["Free"]["PostedregualAds"]=Product.objects.filter(user_id=userId).filter(plan="Free").filter(adsType="Regular").count()
                finalObj["planDataDetails"]["Free"]["leftRegularAds"]=3*planObj["free"]-Product.objects.filter(user_id=userId).filter(plan="Free").filter(adsType="Regular").count()
                finalObj["planDataDetails"]["Free"]["limitDays"]=7
                finalObj["postAdsForm"]["Free"]={}
                finalObj["postAdsForm"]["Free"]["category"]=[]
                tempVal=False
                if finalObj["planDataDetails"]["Free"]["leftRegularAds"] >0:
                    tempVal=True
                    finalObj["postAdsForm"]["Free"]["category"].append("Regular")
                if tempVal:
                    finalObj["leftPlan"].append("Free")
                finalObj["postAdsForm"]["Free"]["days"]=7
            elif plan=="Silver":
                finalObj["planDataDetails"]["Silver"]={}
                finalObj["planDataDetails"]["Silver"]["totalAds"]=5
                finalObj["planDataDetails"]["Silver"]["reponse"]="Unlimitd"
                finalObj["planDataDetails"]["Silver"]["limitDays"]=15
                finalObj["planDataDetails"]["Silver"]["PostedregualAds"]=Product.objects.filter(user=userId).filter(plan="Silver").filter(adsType="Regular").count()
                finalObj["planDataDetails"]["Silver"]["leftRegularAds"]=5*planObj["Silver"]-Product.objects.filter(user=userId).filter(plan="Silver").filter(adsType="Regular").count()
                # finalObj["planDataDetails"]["Silver"]["PostedTopAds"]=Product.objects.filter(user=userId).filter(plan="Silver").filter(adsType="TopAds").count()
                # finalObj["planDataDetails"]["Silver"]["leftTopAds"]=2*planObj["Silver"]-Product.objects.filter(user=userId).filter(plan="Silver").filter(adsType="TopAds").count()
                # finalObj["planDataDetails"]["Silver"]["PostedFeaturedAds"]=Product.objects.filter(user=userId).filter(plan="Silver").filter(adsType="Featured").count()
                # finalObj["planDataDetails"]["Silver"]["leftFeaturedAds"]=3*planObj["Silver"]-Product.objects.filter(user=userId).filter(plan="Silver").filter(adsType="Featured").count()
                finalObj["planDataDetails"]["Silver"]["validity"] = 90  # Adding the validity field with 90 days value
                finalObj["planDataDetails"]["Silver"]["TeleSupport"]=True
                finalObj["planDataDetails"]["Silver"]["chatSupport"] = True
                

                #for post add form
                tempVal=False
                finalObj["postAdsForm"]["Silver"]={}
                finalObj["postAdsForm"]["Silver"]["category"]=[]
                if finalObj["planDataDetails"]["Silver"]["leftRegularAds"] >0:
                    tempVal=True
                    finalObj["postAdsForm"]["Silver"]["category"].append("Regular")
                # if finalObj["planDataDetails"]["Silver"]["leftTopAds"] >0:
                #     tempVal=True
                #     finalObj["postAdsForm"]["Silver"]["category"].append("TopAds")
                # if finalObj["planDataDetails"]["Silver"]["leftFeaturedAds"] >0:
                #     tempVal=True
                #     finalObj["postAdsForm"]["Silver"]["category"].append("Featured")
                
                if tempVal:
                    finalObj["leftPlan"].append("Silver")
                finalObj["postAdsForm"]["Silver"]["days"]=15
                
                
    #             elif plan == "Silver":
    # finalObj["planDataDetails"]["Silver"] = {}
    # finalObj["planDataDetails"]["Silver"]["totalAds"] = 5
    # finalObj["planDataDetails"]["Silver"]["reponse"] = "Unlimited"
    # finalObj["planDataDetails"]["Silver"]["limitDays"] = 15
    # finalObj["planDataDetails"]["Silver"]["validity"] = 90  # Adding the validity field with 90 days value
    # finalObj["planDataDetails"]["Silver"]["TeleSupport"] = True
    # finalObj["planDataDetails"]["Silver"]["chatSupport"] = True


            elif plan=="Gold":
                finalObj["planDataDetails"]["Gold"]={}
                finalObj["planDataDetails"]["Gold"]["totalAds"]=10
                finalObj["planDataDetails"]["Gold"]["reponse"]="Unlimitd"
                finalObj["planDataDetails"]["Gold"]["limitDays"]=30
                finalObj["planDataDetails"]["Gold"]["PostedregualAds"]=Product.objects.filter(user=userId).filter(plan="Gold").filter(adsType="Regular").count()
                finalObj["planDataDetails"]["Gold"]["leftRegularAds"]=10*planObj["Gold"]-Product.objects.filter(user=userId).filter(plan="Gold").filter(adsType="Regular").count()
                # finalObj["planDataDetails"]["Gold"]["PostedTopAds"]=Product.objects.filter(user=userId).filter(plan="Gold").filter(adsType="TopAds").count()
                # finalObj["planDataDetails"]["Gold"]["leftTopAds"]=5*planObj["Gold"]-Product.objects.filter(user=userId).filter(plan="Gold").filter(adsType="TopAds").count()
                # finalObj["planDataDetails"]["Gold"]["PostedFeaturedAds"]=Product.objects.filter(user=userId).filter(plan="Gold").filter(adsType="Featured").count()
                # finalObj["planDataDetails"]["Gold"]["leftFeaturedAds"]=5*planObj["Gold"]-Product.objects.filter(user=userId).filter(plan="Gold").filter(adsType="Featured").count()
                finalObj["planDataDetails"]["Gold"]["validity"] = 90  # Adding the validity field with 90 days value
                finalObj["planDataDetails"]["Gold"]["TeleSupport"]=True
                finalObj["planDataDetails"]["Gold"]["chatSupport"]=True
                finalObj["planDataDetails"]["Gold"]["DeticatedRm"]=True
                finalObj["planDataDetails"]["Gold"]["Hol9Web"]=True


                #for post add form
                tempVal=False
                finalObj["postAdsForm"]["Gold"]={}
                finalObj["postAdsForm"]["Gold"]["category"]=[]
                if finalObj["planDataDetails"]["Gold"]["leftRegularAds"] >0:
                    tempVal=True
                    finalObj["postAdsForm"]["Gold"]["category"].append("Regular")
                # if finalObj["planDataDetails"]["Gold"]["leftTopAds"] >0:
                #     tempVal=True
                #     finalObj["postAdsForm"]["Gold"]["category"].append("TopAds")
                # if finalObj["planDataDetails"]["Gold"]["leftFeaturedAds"] >0:
                #     tempVal=True
                #     finalObj["postAdsForm"]["Gold"]["category"].append("Featured")
                if tempVal:
                    finalObj["leftPlan"].append("Gold")
                finalObj["postAdsForm"]["Gold"]["days"]=30

            elif plan=="Platinum":
                finalObj["planDataDetails"]["Platinum"]={}
                finalObj["planDataDetails"]["Platinum"]["totalAds"]=15
                finalObj["planDataDetails"]["Platinum"]["reponse"]="Unlimitd"
                finalObj["planDataDetails"]["Platinum"]["limitDays"]=60
                finalObj["planDataDetails"]["Platinum"]["PostedregualAds"]=Product.objects.filter(user=userId).filter(plan="Platinum").filter(adsType="Regular").count()
                finalObj["planDataDetails"]["Platinum"]["leftRegularAds"]=15*planObj["Platinum"]-Product.objects.filter(user=userId).filter(plan="Platinum").filter(adsType="Regular").count()
                # finalObj["planDataDetails"]["Platinum"]["PostedTopAds"]=Product.objects.filter(user=userId).filter(plan="Platinum").filter(adsType="TopAds").count()
                # finalObj["planDataDetails"]["Platinum"]["leftTopAds"]=5*planObj["Platinum"]-Product.objects.filter(user=userId).filter(plan="Platinum").filter(adsType="TopAds").count()
                # finalObj["planDataDetails"]["Platinum"]["PostedFeaturedAds"]=Product.objects.filter(user=userId).filter(plan="Platinum").filter(adsType="Featured").count()
                # finalObj["planDataDetails"]["Platinum"]["leftFeaturedAds"]=5*planObj["Platinum"]-Product.objects.filter(user=userId).filter(plan="Platinum").filter(adsType="Featured").count()
                finalObj["planDataDetails"]["Platinum"]["validity"] = 90  # Adding the validity field with 90 days value
                finalObj["planDataDetails"]["Platinum"]["TeleSupport"]=True
                finalObj["planDataDetails"]["Platinum"]["chatSupport"]=True
                finalObj["planDataDetails"]["Platinum"]["DeticatedRm"]=True
                finalObj["planDataDetails"]["Platinum"]["Hol9Web"]=True

                #for post add form
                tempVal=False
                finalObj["postAdsForm"]["Platinum"]={}
                finalObj["postAdsForm"]["Platinum"]["category"]=[]
                if finalObj["planDataDetails"]["Platinum"]["leftRegularAds"] >0:
                    tempVal=True
                    finalObj["postAdsForm"]["Platinum"]["category"].append("Regular")   
                # if finalObj["planDataDetails"]["Platinum"]["leftTopAds"] >0:
                #     tempVal=True
                #     finalObj["postAdsForm"]["Platinum"]["category"].append("TopAds")
                # if finalObj["planDataDetails"]["Platinum"]["leftFeaturedAds"] >0:
                #     tempVal=True
                #     finalObj["postAdsForm"]["Platinum"]["category"].append("Featured")
                if tempVal:
                    finalObj["leftPlan"].append("Platinum")
                finalObj["postAdsForm"]["Platinum"]["days"]=30
                finalObj["postAdsForm"]["Platinum"]["days"]=60
        print(finalObj)
        result2=json.dumps(finalObj)
        return HttpResponse(result2, content_type='application/json')

import json

class getExtraCat(APIView):
    def post( self,request , format=None):
        category=request.data.get("category")
        subcategory=request.data.get("subcategory")
        json1_file = open('/hola9Main/hola9DjangoLatest/adsapi/json/subcategory.json','r+', encoding="utf-8")
        obj=json.load(json1_file)
        print(list[obj.keys()])
        if category and subcategory:
            result2=json.dumps(obj[category][subcategory])
        elif category:
            result2=json.dumps(list(obj[category].keys()))
        print(result2)
        return HttpResponse(result2, content_type='application/json')

import time
import datetime

from datetime import date, timedelta

def jobEveryDAYRun(request):
    s=datetime.datetime.now().strftime('%y-%m-%d')
    print(s)
    p=True
    sDetla=Product.objects.filter(date_expire="null")
    if sDetla:
        for result in sDetla:
            if isinstance(result.DaysLimit, int):
                print(result.date_created)
                if "/" in result.date_created:
                    pass
                elif "-" in result.date_created:  
                    result.date_expire=datetime.datetime.strptime(result.date_created, '%Y-%m-%d') + timedelta(days=result.DaysLimit)
                result.save()
    while(p):
        if not CurrentDate.objects.filter(dateFiled=str(s)):
            modelUpdate=CurrentDate.objects.create(dateFiled=s)
            productData=Product.objects.all()
            for x in productData:
                if x.DaysLimit==0:
                    x.expiry=True
                else:
                    x.DaysLimit=x.DaysLimit-1
                x.save()
        p=False
        print("hello wrold")
    return HttpResponse("success", content_type='application/json')
class webpopuplist(APIView):
    def post(self,request,format=None):
        dateads= request.data.get("dateads")
        idvalues=request.data.get("id")
        s={}
        if dateads=="User":
            s=User.objects.filter(pk=idvalues)   
        elif dateads=="Product":
            s=Product.objects.filter(pk=idvalues)
        elif dateads == "TelemetryDaa":
            s=TelemetryDaa.objects.filter(pk=idvalues)
        elif dateads == "ReviewSection":
            s=ReviewSection.objects.filter(pk=idvalues)
        elif dateads == "JobApply":
            s=JobApply.objects.filter(pk=idvalues)
        elif dateads == "JobsRequired":
            s=JobsRequired.objects.filter(pk=idvalues)
        elif dateads == "Pricing":
            s=Pricing.objects.filter(pk=idvalues)
        elif dateads == "PaymentDetailsValues":
            s=PaymentDetailsValues.objects.filter(pk=idvalues)
        elif dateads == "RealEstateEnquery":
            s=RealEstateEnquery.objects.filter(pk=idvalues)
        elif dateads == "Blogs":
            s=Blogs.objects.filter(pk=idvalues)
        elif dateads == "BlogComment":
            s=BlogComment.objects.filter(pk=idvalues)
        elif dateads == "AdsComment":
            s=AdsComment.objects.filter(pk=idvalues)
        elif dateads == "Contact":
            s=Contact.objects.filter(pk=idvalues)
        elif dateads == "Profile":
            s=Profile.objects.filter(pk=idvalues)
        elif dateads == "Order":
            s=Order.objects.filter(pk=idvalues)
        elif dateads == "TransationIdone":
            s=TransationIdone.objects.filter(pk=idvalues)
        elif dateads == "adsmangeme":
            s=adsmangeme.objects.filter(pk=idvalues)
        elif dateads == "OTPVerifiaction":
            s=OTPVerifiaction.objects.filter(pk=idvalues)
        elif dateads == "AdminAuth":
            s=AdminAuth.objects.filter(pk=idvalues)
        elif dateads == "LastLogin":
            s=LastLogin.objects.filter(pk=idvalues)
        elif dateads == "ReportAds":
            s=ReportAds.objects.filter(pk=idvalues)

        data=serializers.serialize('json',s)   
        return HttpResponse(data,content_type='application/json')

class DeletedAds(APIView):
    def post( self,request , format=None):
        adsid=request.data.get("adsId")
        ads=Product.objects.get(pk=adsid)
        ads.deleted=True
        ads.expiry=True
        ads.DaysLimit=0
        ads.save()
        return HttpResponse("success", content_type='application/json')

import json
class searchData(APIView):
    def post( self,request , format=None):
        s=Product.objects.all().values('title')
        list_result = [entry["title"] for entry in s] 
        listvalue=[]
        for  x in list_result:
            obj={}
            obj["value"]=x
            listvalue.append(obj)
        print(list_result)
        return HttpResponse(json.dumps(listvalue), content_type='application/json')


class approveAds(APIView):
    def post( self,request , format=None):
        idValue=request.data.get('idValue')
        if not idValue:
            s=Product.objects.filter(is_active=False)
            data=serializers.serialize('json',s)
        else:
            s=Product.objects.get(pk=idValue)
            s.is_active=True
            s.save()
            data="success"
        return HttpResponse(data, content_type='application/json')
  

class SearchAdsWithSort(APIView):
    def post (self,request,format=None):
        sortValue=request.data.get("shortValue")
        titleValue=request.data.get("titleValue")
        print(sortValue,titleValue)
        start=request.data.get('start')
        end=request.data.get('end')
        ads=request.data.get('ads')
        if ads=="all":
            data=Product.objects.filter(is_active=True)[int(start):int(end)]
            return HttpResponse(serializers.serialize('json',data), content_type='application/json')
        if titleValue and sortValue:
            print("both")
            if sortValue=="MinToMax":
                s=Product.objects.filter(title__icontains=titleValue).filter(is_active=True).order_by('price')
            elif sortValue=="MaxToMin":
                s=Product.objects.filter(title__icontains=titleValue).filter(is_active=True).order_by('-price')
            elif sortValue=="Fetured":
                s=Product.objects.filter(title__icontains=titleValue).filter(is_active=True).exclude(plan="Free")
            else:
                s=Product.objects.filter(is_active=True)
        elif titleValue:
            print("title onlye")
            s=Product.objects.filter(title__icontains=titleValue).filter(is_active=True)
        elif sortValue:
            print("sort value only")
            if sortValue=="MinToMax":
                s=Product.objects.filter(is_active=True).order_by('price')
            elif sortValue=="MaxToMin":
                s=Product.objects.filter(is_active=True).order_by('-price')
            elif sortValue=="Fetured":
                s=Product.objects.filter(is_active=True).exclude(plan="Free")
            else:
                s=Product.objects.filter(is_active=True)
        print(s.order_by('-date_created'))
        for x in s:
            print(x.pk,x.price)
        # s=s.order_by('-date_created')
        return HttpResponse(serializers.serialize('json',s[int(start):int(end)]), content_type='application/json')


class SearchWeb(APIView):
    def post( self,request , format=None):
        searchValue=request.data.get("searchValue")
        start=request.data.get('start')
        end=request.data.get('end')
        if searchValue=="":
            return HttpResponse(json.dumps([]), content_type='application/json')
        results = Product.search(searchValue)
        if len(results)==0:
            return HttpResponse(json.dumps({"message":"Data Not Found"}), content_type='application/json')
        for x in results:
            print(x.City)
        return HttpResponse(serializers.serialize('json',results[int(start):int(end)]), content_type='application/json')


# import json
# class CheckBusinessPlan(APIView):
#     def post( self,request , format=None):
#         s1={"businessPlan":False}
#         userid=request.data.get("userid")
#         s=BusinessPricing.objects.filter(user_id=userid)
#         if s:
#             s1["businessPlan"]=True
#         s1["Plan"]=serializers.serialize('json',BusinessPricing.objects.filter(user_id=userid))
#         return HttpResponse(json.dumps(s1), content_type='application/json')

# import json
# from django.http import JsonResponse

# class CheckBusinessPlan(APIView):
#     def post(self, request, format=None):
#         s1 = {"businessPlan": False}
#         userid = request.data.get("userid")
#         s = BusinessPricing.objects.filter(user_id=userid)
        
#         if s:
#             s1["businessPlan"] = True
        
#         plans = [
#             {
#                 # "model": "adsapi.businesspricing",
#                 "pk": plan.pk,
#                 "fields": {
#                     "user": plan.user_id,
#                     "OrderID": plan.OrderID,
#                     "category": plan.category,
#                     "validity": plan.validity,
#                     "city": plan.city,
#                     "visiblity": plan.visiblity,
#                     "NoAds": plan.NoAds,
#                     "teleSupport": plan.teleSupport,
#                     "chatSupport": plan.chatSupport,
#                     "dedicatedRm": plan.dedicatedRm,
#                     "hol9Website": plan.hol9Website,
#                 }
#             }
#             for plan in s
#         ]
        
#         s1["Plan"] = plans
#         return JsonResponse(s1)


# *********************************************************************************

# class CheckBusinessPlan(APIView):
#     def post(self, request, format=None):
#         s1 = {"businessPlan": False}
#         userid = request.data.get("userid")
#         s = BusinessPricing.objects.filter(user_id=userid)
        
#         if s:
#             s1["businessPlan"] = True
        
#         plans = [
#             {
#                 "pk": plan.pk,
#                 "fields": {
#                     "user": plan.user_id,
#                     "OrderID": plan.OrderID,
#                     "category": plan.category,
#                     "validity": plan.validity,
#                     "city": plan.city,
#                     "visiblity": plan.visiblity,
#                     "NoAds": plan.NoAds,
#                     "teleSupport": plan.teleSupport,
#                     "chatSupport": plan.chatSupport,
#                     "dedicatedRm": plan.dedicatedRm,
#                     "hol9Website": plan.hol9Website,
#                 }
#             }
#             for plan in s
#         ]
        
#         # Calculate total ads for each plan category
#         total_ads_by_category = {}
#         for plan in plans:
#             category = plan["fields"]["category"]
#             no_ads = int(plan["fields"]["NoAds"])
#             if category in total_ads_by_category:
#                 total_ads_by_category[category] += no_ads
#             else:
#                 total_ads_by_category[category] = no_ads
            
#             # Include total ads for the current plan category in the fields
#             plan["fields"]["totalAdsInCategory"] = total_ads_by_category[category]
            
#             # Include posted and remaining Premium ads for Premium plan
#             if category == "Premium":
#                 user_id = plan["fields"]["user"]
#                 posted_premium_ads = Product.objects.filter(user=user_id, plan="Premium").count()
#                 left_premium_ads = no_ads - posted_premium_ads
#                 plan["fields"]["postedPremiumAds"] = posted_premium_ads
#                 plan["fields"]["leftPremiumAds"] = left_premium_ads
            
#             # Include posted and remaining Featured ads for Featured plan
#             if category == "Featured":
#                 user_id = plan["fields"]["user"]
#                 posted_featured_ads = Product.objects.filter(user=user_id, plan="Featured").count()
#                 left_featured_ads = no_ads - posted_featured_ads
#                 plan["fields"]["postedFeaturedAds"] = posted_featured_ads
#                 plan["fields"]["leftFeaturedAds"] = left_featured_ads
        
#         s1["Plan"] = plans
        
#         return JsonResponse(s1)

# class CheckBusinessPlan(APIView):
#     def post(self, request, format=None):
#         s1 = {"businessPlan": False, "leftPlan": []}
#         userid = request.data.get("userid")
#         s = BusinessPricing.objects.filter(user_id=userid)
        
#         if s:
#             s1["businessPlan"] = True
        
#         plans = [
#             {
#                 "fields": {
#                     "user": plan.user_id,
#                     "OrderID": plan.OrderID,
#                     "category": plan.category,
#                     "validity": plan.validity,
#                     "city": plan.city,
#                     "visiblity": plan.visiblity,
#                     "NoAds": plan.NoAds,
#                     "teleSupport": plan.teleSupport,
#                     "chatSupport": plan.chatSupport,
#                     "dedicatedRm": plan.dedicatedRm,
#                     "hol9Website": plan.hol9Website,
#                 }
#             }
#             for plan in s
#         ]
        
#         # Calculate total ads for each plan category
#         total_ads_by_category = {}
#         for plan in plans:
#             category = plan["fields"]["category"]
#             no_ads = int(plan["fields"]["NoAds"])
#             if category in total_ads_by_category:
#                 total_ads_by_category[category] += no_ads
#             else:
#                 total_ads_by_category[category] = no_ads
            
#             # Include total ads for the current plan category in the fields
#             plan["fields"]["totalAdsInCategory"] = total_ads_by_category[category]
            
#             # Include posted and remaining Premium ads for Premium plan
#             if category == "Premium":
#                 user_id = plan["fields"]["user"]
#                 posted_premium_ads = Product.objects.filter(user=user_id, plan="Premium").count()
#                 left_premium_ads = no_ads - posted_premium_ads
#                 plan["fields"]["postedPremiumAds"] = posted_premium_ads
#                 plan["fields"]["leftPremiumAds"] = left_premium_ads
            
#                 # If there are remaining premium ads, add the category to the "leftPlan" list
#                 if left_premium_ads > 0 and "Premium" not in s1["leftPlan"]:
#                     s1["leftPlan"].append("Premium")
            
#             # Include posted and remaining Featured ads for Featured plan
#             if category == "Featured":
#                 user_id = plan["fields"]["user"]
#                 posted_featured_ads = Product.objects.filter(user=user_id, plan="Featured").count()
#                 left_featured_ads = no_ads - posted_featured_ads
#                 plan["fields"]["postedFeaturedAds"] = posted_featured_ads
#                 plan["fields"]["leftFeaturedAds"] = left_featured_ads
            
#                 # If there are remaining featured ads, add the category to the "leftPlan" list
#                 if left_featured_ads > 0 and "Featured" not in s1["leftPlan"]:
#                     s1["leftPlan"].append("Featured")
        
#         s1["Plan"] = plans
        
#         return JsonResponse(s1)

# class CheckBusinessPlan(APIView):
#     def post(self, request, format=None):
#         s1 = {"businessPlan": False, "leftPlan": [], "totalPlan": []}
#         userid = request.data.get("userid")
#         s = BusinessPricing.objects.filter(user_id=userid)
        
#         if s:
#             s1["businessPlan"] = True
        
#         plans = [
#             {
#                 "fields": {
#                     "user": plan.user_id,
#                     "OrderID": plan.OrderID,
#                     "category": plan.category,
#                     "validity": plan.validity,
#                     "city": plan.city,
#                     "visiblity": plan.visiblity,
#                     "NoAds": plan.NoAds,
#                     "teleSupport": plan.teleSupport,
#                     "chatSupport": plan.chatSupport,
#                     "dedicatedRm": plan.dedicatedRm,
#                     "hol9Website": plan.hol9Website,
#                 }
#             }
#             for plan in s
#         ]
        
#         # Calculate total ads for each plan category
#         total_ads_by_category = {}
#         for plan in plans:
#             category = plan["fields"]["category"]
#             no_ads = int(plan["fields"]["NoAds"])
#             if category in total_ads_by_category:
#                 total_ads_by_category[category] += no_ads
#             else:
#                 total_ads_by_category[category] = no_ads
            
#             # Include total ads for the current plan category in the fields
#             plan["fields"]["totalAdsInCategory"] = total_ads_by_category[category]
            
#             # If there are remaining ads, add the category to the "leftPlan" list
#             if no_ads > 0 and category not in s1["leftPlan"]:
#                 s1["leftPlan"].append(category)
            
#             # If the category is not already in the "totalPlan" list, add it
#             if category not in s1["totalPlan"]:
#                 s1["totalPlan"].append(category)
            
#             # Include posted and remaining Premium ads for Premium plan
#             if category == "Premium":
#                 user_id = plan["fields"]["user"]
#                 posted_premium_ads = Product.objects.filter(user=user_id, plan="Premium").count()
#                 left_premium_ads = no_ads - posted_premium_ads
#                 plan["fields"]["postedPremiumAds"] = posted_premium_ads
#                 plan["fields"]["leftPremiumAds"] = left_premium_ads
            
#             # Include posted and remaining Featured ads for Featured plan
#             if category == "Featured":
#                 user_id = plan["fields"]["user"]
#                 posted_featured_ads = Product.objects.filter(user=user_id, plan="Featured").count()
#                 left_featured_ads = no_ads - posted_featured_ads
#                 plan["fields"]["postedFeaturedAds"] = posted_featured_ads
#                 plan["fields"]["leftFeaturedAds"] = left_featured_ads
        
#         s1["Plan"] = plans
        
#         return JsonResponse(s1)
# *******************************************************************************
# ********************************************************************************

# class CheckBusinessPlan(APIView):
#     def post(self, request, format=None):
#         s1 = {
#             "businessPlan": False,
#             "leftPlan": [],
#             "totalPlan": [],
#             "numberOfTimePlan": {}
#         }
#         userid = request.data.get("userid")
#         s = BusinessPricing.objects.filter(user_id=userid)
        
#         if s:
#             s1["businessPlan"] = True
        
#         plans = [
#             {
#                 "fields": {
#                     "user": plan.user_id,
#                     "OrderID": plan.OrderID,
#                     "category": plan.category,
#                     "validity": plan.validity,
#                     "city": plan.city,
#                     "visiblity": plan.visiblity,
#                     "NoAds": plan.NoAds,
#                     "teleSupport": plan.teleSupport,
#                     "chatSupport": plan.chatSupport,
#                     "dedicatedRm": plan.dedicatedRm,
#                     "hol9Website": plan.hol9Website,
#                 }
#             }
#             for plan in s
#         ]
        
#         # Calculate total ads for each plan category
#         total_ads_by_category = {}
#         number_of_times_plan = {}
        
#         for plan in plans:
#             category = plan["fields"]["category"]
#             no_ads = int(plan["fields"]["NoAds"])
            
#             # Increment the count for the current plan category
#             if category in number_of_times_plan:
#                 number_of_times_plan[category] += 1
#             else:
#                 number_of_times_plan[category] = 1
            
#             if category in total_ads_by_category:
#                 total_ads_by_category[category] += no_ads
#             else:
#                 total_ads_by_category[category] = no_ads
            
#             # Include total ads for the current plan category in the fields
#             plan["fields"]["totalAdsInCategory"] = total_ads_by_category[category]
            
#             # If there are remaining ads, add the category to the "leftPlan" list
#             if no_ads > 0 and category not in s1["leftPlan"]:
#                 s1["leftPlan"].append(category)
            
#             # If the category is not already in the "totalPlan" list, add it
#             if category not in s1["totalPlan"]:
#                 s1["totalPlan"].append(category)
            
#             # Include posted and remaining Premium ads for Premium plan
#             if category == "Premium":
#                 user_id = plan["fields"]["user"]
#                 posted_premium_ads = Product.objects.filter(user=user_id, plan="Premium").count()
#                 left_premium_ads = no_ads - posted_premium_ads
#                 plan["fields"]["postedPremiumAds"] = posted_premium_ads
#                 plan["fields"]["leftPremiumAds"] = left_premium_ads
            
#             # Include posted and remaining Featured ads for Featured plan
#             if category == "Featured":
#                 user_id = plan["fields"]["user"]
#                 posted_featured_ads = Product.objects.filter(user=user_id, plan="Featured").count()
#                 left_featured_ads = no_ads - posted_featured_ads
#                 plan["fields"]["postedFeaturedAds"] = posted_featured_ads
#                 plan["fields"]["leftFeaturedAds"] = left_featured_ads
        
#         s1["Plan"] = plans
#         s1["numberOfTimePlan"] = number_of_times_plan
        
#         return JsonResponse(s1)

import json
from django.http import JsonResponse
from .models import BusinessPricing  # Import your BusinessPricing model
from .models import Product  # Import your Product model

class CheckBusinessPlan(APIView):
    def post(self, request, format=None):
        response_data = {
            "businessPlan": False,  # Initialize as False
            "planDataDetails": {},
            "postAdsForm": {},
            "leftPlan": [],
            "totalPlan": [],
            "numberOfTimePlan": {}
        }
        
        userid = request.data.get("userid")
        plans = BusinessPricing.objects.filter(user_id=userid)
        
        if plans:
            response_data["businessPlan"] = True  # Set to True if plans exist
            response_data["planDataDetails"] = self.generate_plan_data_details(plans)
            response_data["postAdsForm"] = self.generate_post_ads_form(plans)
            response_data["leftPlan"] = self.generate_left_plan(plans)
            response_data["totalPlan"] = self.generate_total_plan(plans)
            response_data["numberOfTimePlan"] = self.generate_number_of_time_plan(plans)
        
        return JsonResponse(response_data)
    
    # def generate_plan_data_details(self, plans):
    #     plan_data_details = {}
        
    #     for plan in plans:
    #         category = plan.category.lower()  # Convert category to lowercase for consistency
            
    #         if category in plan_data_details:
    #             plan_data_details[category]["totalAds"] += int(plan.NoAds)
    #         else:
    #             plan_data_details[category] = {
    #                 "totalAds": int(plan.NoAds),
    #                 "reponse": "Unlimited",  # Modify as needed
    #                 "limitDays": int(plan.validity),
    #                 "PostedregualAds": 0,
    #                 "leftRegularAds": int(plan.NoAds),
    #                 "validity": int(plan.validity),
    #                 "TeleSupport": plan.teleSupport,
    #                 "chatSupport": plan.chatSupport
    #             }
                
    #             if plan.dedicatedRm:
    #                 plan_data_details[category]["DeticatedRm"] = plan.dedicatedRm
    #             if plan.hol9Website:
    #                 plan_data_details[category]["Hol9Web"] = plan.hol9Website
        
    #     return plan_data_details
    def generate_plan_data_details(self, plans):
        plan_data_details = {}
    
        for plan in plans:
            category = plan.category.lower()
        
            if category in plan_data_details:
                plan_data_details[category]["totalAds"] += int(plan.NoAds)
                plan_data_details[category]["leftRegularAds"] = (
                    plan_data_details[category]["totalAds"] - plan_data_details[category]["PostedregualAds"]
                )
            else:
                plan_data_details[category] = {
                    "totalAds": int(plan.NoAds),
                    "reponse": "Unlimited",
                    "limitDays": int(plan.validity),
                    "PostedregualAds": 0,
                    "leftRegularAds": int(plan.NoAds),  # Initially all ads are left
                    "validity": int(plan.validity),
                    "TeleSupport": plan.teleSupport,
                    "chatSupport": plan.chatSupport
                }
            
                if plan.dedicatedRm:
                    plan_data_details[category]["DeticatedRm"] = plan.dedicatedRm
                if plan.hol9Website:
                    plan_data_details[category]["Hol9Web"] = plan.hol9Website
    
        return plan_data_details
    
    def generate_post_ads_form(self, plans):
        post_ads_form = {}
        
        for plan in plans:
            category = plan.category.lower()
            post_ads_form[category] = {
                "category": ["Regular"],  # Modify as needed
                "days": int(plan.validity)
            }
        
        return post_ads_form
    
    def generate_left_plan(self, plans):
        left_plan = []
        
        for plan in plans:
            category = plan.category.lower()
            if int(plan.NoAds) > 0 and category not in left_plan:
                left_plan.append(category)
        
        return left_plan
    
    def generate_total_plan(self, plans):
        total_plan = list(set([plan.category.lower() for plan in plans]))
        return total_plan
    
    def generate_number_of_time_plan(self, plans):
        number_of_time_plan = {}
        
        for plan in plans:
            category = plan.category.lower()
            if category in number_of_time_plan:
                number_of_time_plan[category] += 1
            else:
                number_of_time_plan[category] = 1
        
        return number_of_time_plan



class BusinessAds(APIView):
    def post( self,request , format=None):
        s1={"businessPlan":False}
        userid=request.data.get("userid")
        s=BusinessPricing.objects.filter(user_id=userid)
        if s:
            s1["businessPlan"]=True
        s1["Premium"]=serializers.serialize('json',Product.objects.filter(PlanCategory="Premium"))
        s1["Featured"]=serializers.serialize('json',Product.objects.filter(PlanCategory="Featured"))
        return HttpResponse(json.dumps(s1), content_type='application/json')
from rest_framework import generics


    
class BusinessProfiles(viewsets.ModelViewSet):
    queryset = BusinessProfile.objects.all()
    serializer_class = BusinessProfileSerializer

    def get_queryset(self):
        # Get the 'limit' parameter from the query parameters
        limit = self.request.query_params.get('limit', None)

        # Apply the limit if it's a valid positive integer
        if limit is not None and limit.isdigit() and int(limit) > 0:
            # return BusinessProfile.objects.all()[:int(limit)]
            return BusinessProfile.objects.all().order_by('-id')[:int(limit)]

        else:
            return BusinessProfile.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
class BusinessProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BusinessProfile.objects.all()
    serializer_class = BusinessProfileSerializer
    
    def get_serializer(self, *args, **kwargs):
        # Set partial argument based on the HTTP method
        kwargs['partial'] = self.request.method in ['PATCH', 'PUT']
        return super().get_serializer(*args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Deleted successfully"}, status=status.HTTP_200_OK)

class MybusinessPlan(APIView):
    def post( self,request , format=None):
        s1={"businessPlan":False}
        userid=request.data.get("userid")
        s=BusinessPricing.objects.filter(user_id=userid)
        if s:
            s1["businessPlan"]=True
        s1["Premium"]=serializers.serialize('json',Product.objects.filter(PlanCategory="Premium"))
        s1["Featured"]=serializers.serialize('json',Product.objects.filter(PlanCategory="Featured"))
        return HttpResponse(serializers.serialize('json',Product.objects.filter(PlanCategory="Featured")), content_type='application/json')


class CheckVerified(APIView):
    def post( self,request , format=None):
        s1={"verifiedCustomer":False}
        userid=request.data.get("userid")
        s=VerifiedCustomerMain.objects.filter(userid=userid)
        if s:
            s1["verifiedCustomer"]=True
        return HttpResponse(json.dumps(s1), content_type='application/json')

class CollectVisitPhoneNumber(APIView):
    def post( self,request , format=None):
        s1={"success":True}
        productID=request.data.get("productID")
        phoneNumber=request.data.get('phoneNubmer')
        s=Product.objects.get(pk=productID)
        if not s.phoneNumberCollectVisiters:
            s.phoneNumberCollectVisiters=""
            s.phoneNumberCollectVisiters=s.phoneNumberCollectVisiters+phoneNumber+','
        else:
            s.phoneNumberCollectVisiters=s.phoneNumberCollectVisiters+phoneNumber+','
        s.save()
        return HttpResponse(json.dumps(s1), content_type='application/json')




from rest_framework.response import Response
from rest_framework.views import APIView
from .models import BusinessProfile  # Import your model if not already imported

class BusinessVerifiedAPI(APIView):
    def post(self, request):
        email = request.data.get('email')  # Get the email from the POST data
        
        try:
            business_profile = BusinessProfile.objects.get(email=email, is_verified=True)
            response_data = {
                'business_profile_verified': True,
                'name': business_profile.name,
                'company_name': business_profile.company_name,
                'email': business_profile.email,
                'phone_number': business_profile.phone_number,
            }
            return Response(response_data)
        except BusinessProfile.DoesNotExist:
            return Response({'business_profile_verified': False})

from rest_framework import status
class EmployeeLoginView2(APIView):
    def get(self, request):
        employees = EmployeeLogin2.objects.all()
        serializer = EmployeeLogin2Serializer2(employees, many=True)
        return Response(serializer.data)
     
    def post(self, request):
        serializer = EmployeeLogin2Serializer2(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class  EmployeeLoginUpdateDelete2(APIView):
    def put(self,request,pk):
        employee2 = EmployeeLogin2.objects.get(pk=pk)
        serializer = EmployeeLogin2Serializer2(employee2,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
   
    def delete(self,request,pk):
        employee_login = EmployeeLogin2.objects.get(pk=pk)
        employee_login.delete()
        return Response({"message": "deleted successfully."},status=status.HTTP_204_NO_CONTENT)
    

class AssignTaskView(APIView):
    def get(self, request):
        assign_task = AssignTask.objects.all()
        serializer = AssignTaskSerializer(assign_task, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = AssignTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class  AssignTaskUpdateDelete(APIView):
    def put(self,request,pk):
        assign_task = AssignTask.objects.get(pk=pk)
        serializer = AssignTaskSerializer(assign_task,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
   
    def delete(self,request,pk):
        assign_task = AssignTask.objects.get(pk=pk)
        assign_task.delete()
        return Response({"message": "deleted successfully !"},status=status.HTTP_204_NO_CONTENT)
    
    
from account.serializers import UserSerializer
from profileapi.serializers import ProfileSerializer

# class TopSellerAdsView(APIView):
#     def get(self, request, format=None):
#         try:
#             # Get top 30 sellers with ads posted
#             top_sellers = User.objects.filter(total_ads_posted__gt=0).order_by('-total_ads_posted')[:50]

#             # Serialize the data including user's image and created_at
#             serialized_data = []
#             for user in top_sellers:
#                 user_data = UserSerializer(user).data

#                 # Retrieve the user's profile
#                 try:
#                     profile = Profile.objects.get(user=user)
#                     user_data['image_base64'] = profile.image_base64
#                 except Profile.DoesNotExist:
#                     # Handle the case where the profile does not exist or doesn't have an image field
#                     user_data['image_base64'] = None

#                 # Include the created_at field from the User model
#                 user_data['created_at'] = user.created_at

#                 serialized_data.append(user_data)

#             # Return the serialized data
#             return Response(serialized_data, status=status.HTTP_200_OK)

#         except Exception as e:
#             # Handle exceptions and return an error response
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TopSellerAdsView(APIView):
    def get(self, request, format=None):
        try:
            # Get top sellers with ads posted
            top_sellers = User.objects.filter(total_ads_posted__gt=0).order_by('-total_ads_posted')[:50]

            # Serialize the data including user's image and created_at
            serialized_data = []
            for user in top_sellers:
                user_data = UserSerializer(user).data

                # Retrieve the user's profile
                try:
                    profile = Profile.objects.get(user=user)
                    user_data['image'] = request.build_absolute_uri(profile.image.url) if profile.image else None
                except Profile.DoesNotExist:
                    # Handle the case where the profile does not exist or doesn't have an image field
                    user_data['image'] = None

                # Include the created_at field from the User model
                user_data['created_at'] = user.created_at

                serialized_data.append(user_data)

            # Return the serialized data
            return Response(serialized_data, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle exceptions and return an error response
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




from django.http import JsonResponse
from django.core import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

# class TrendingAds(APIView):
#     def post(self, request, format=None):
#         start = request.data.get("start")
#         end = request.data.get("end")
#         limit = request.data.get("limit")
#         business_plan = request.data.get("businessplan", False)
#         city = request.data.get("city", None)
#         sorting_order = request.data.get("sorting_order", None)
#         search_key = request.data.get("search_key", None)
#         try:
#             start = int(start) if start is not None else None
#             end = int(end) if end is not None else None
#             limit = int(limit) if limit is not None else None
#         except ValueError:
#             return JsonResponse({'error': 'Invalid input values'}, status=400)
#         queryset = Product.objects.all()
#         if business_plan:
#             queryset = queryset.filter(Q(plan="premium") | Q(plan="featured"))
#         if city:
#             queryset = queryset.filter(City=city)
      
#         if sorting_order == 'max_to_min':
#             queryset = queryset.order_by('-price')
#         elif sorting_order == 'min_to_max':
#             queryset = queryset.order_by('price')
#         elif sorting_order == 'recently':
#             queryset = queryset.order_by('-id')
#         elif sorting_order == 'older':
#             queryset = queryset.order_by('id')
#         elif sorting_order == 'default':
#             queryset = queryset.order_by('?')
#         if search_key:
#             search_query = Q()
#             for field in Product._meta.fields:
#                 if field.name != 'image' and field.get_internal_type() in ['CharField', 'TextField', 'DecimalField']:
#                     search_query |= Q(**{f"{field.name}__icontains": search_key})
#             queryset = queryset.filter(search_query)
#         if start is not None and end is not None:
#             count = end - start + 1
#             queryset = queryset.order_by('-id')[start-1:start-1+count]
#         elif limit is not None:
#             if sorting_order == 'max_to_min':
#                 queryset = queryset.order_by('-price')[:limit]
#             elif sorting_order == 'min_to_max':
#                 queryset = queryset.order_by('price')[:limit]
#             elif sorting_order == 'recently':
#                 queryset = queryset.order_by('-id')[:limit]
#             elif sorting_order == 'older':
#                 queryset = queryset.order_by('id')[:limit]
#             elif sorting_order == 'default':
#                 queryset = queryset.order_by('?')[:limit]
#         queryset = queryset.order_by('-viewsproduct')[:50]
#         data = serializers.serialize('json', queryset)
#         top_50_product_ids = [product.id for product in queryset]
#         existing_top_50_products = Top50Products.objects.first()
#         if existing_top_50_products is not None:
#             for product in queryset:
#                 if product.id not in existing_top_50_products.products.values_list('id', flat=True):
#                     message = f"Your Post {product.title} Enter in Top 50 Ads"
#                     user_id = product.user.id if product.user else None
#                     Notification.objects.create(user_id=user_id, message=message)
#         else:
#             existing_top_50_products = Top50Products.objects.create()
#         existing_top_50_products.products.set(top_50_product_ids)
#         return HttpResponse(data, content_type='application/json')
from itertools import chain
import random
class TrendingAds(APIView):
    def post(self, request, format=None):
        start = request.data.get("start")
        end = request.data.get("end")
        limit = request.data.get("limit")
        business_plan = request.data.get("businessplan", False)
        city = request.data.get("city", None)
        sorting_order = request.data.get("sorting_order", None)
        search_key = request.data.get("search_key", None)
        
        try:
            start = int(start) if start is not None else None
            end = int(end) if end is not None else None
            limit = int(limit) if limit is not None else None
        except ValueError:
            return JsonResponse({'error': 'Invalid input values'}, status=400)
        
        queryset = Product.objects.all()
        
        if business_plan:
            queryset = queryset.filter(Q(plan="premium") | Q(plan="featured"))
        
        if city:
            city_queryset = queryset.filter(City=city)
            other_city_queryset = queryset.exclude(City=city)
            city_count = city_queryset.count()
            remaining_limit = 50 - city_count
            if remaining_limit > 0:
                other_city_products = other_city_queryset[:remaining_limit]
                queryset = list(chain(city_queryset, other_city_products))
            else:
                queryset = city_queryset
        else:
            queryset = queryset.order_by('-viewsproduct')[:50]
        
        if sorting_order == 'max_to_min':
            queryset = sorted(queryset, key=lambda x: x.price, reverse=True)
        elif sorting_order == 'min_to_max':
            queryset = sorted(queryset, key=lambda x: x.price)
        elif sorting_order == 'recently':
            queryset = sorted(queryset, key=lambda x: x.id, reverse=True)
        elif sorting_order == 'older':
            queryset = sorted(queryset, key=lambda x: x.id)
        elif sorting_order == 'default':
            queryset = sorted(queryset, key=lambda x: random.random())
        
        if search_key:
            queryset = [product for product in queryset if search_key.lower() in product.title.lower()]
            
        if start is not None and end is not None:
            queryset = queryset[start-1:end]
        elif limit is not None:
            queryset = queryset[:limit]
        
        data = serializers.serialize('json', queryset)
        
        # Notify users if their posts enter the top 50
        top_50_product_ids = [product.id for product in queryset]
        existing_top_50_products = Top50Products.objects.first()
        if existing_top_50_products is not None:
            for product_id in top_50_product_ids:
                if product_id not in existing_top_50_products.products.values_list('id', flat=True):
                    product = Product.objects.get(id=product_id)
                    message = f"Your Post {product.title} Entered in Top 50 Ads"
                    user_id = product.user.id if product.user else None
                    Notification.objects.create(user_id=user_id, message=message)
        else:
            existing_top_50_products = Top50Products.objects.create(products=top_50_product_ids)
            
        return HttpResponse(data, content_type='application/json')



# class NotificationAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         # Get the 'limit' parameter from the query parameters
#         limit = request.query_params.get('limit', None)

#         # Validate and set a default limit if not provided
#         if not limit or not limit.isdigit() or int(limit) <= 0:
#             limit = None

#         # Retrieve notifications based on the limit
#         if limit:
#             notifications = Notification.objects.all().order_by('-created_date')[:int(limit)]
#         else:
#             notifications = Notification.objects.all()

#         serializer = NotificationSerializer(notifications, many=True)

#         return Response(serializer.data, status=status.HTTP_200_OK)

class NotificationAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Get the 'user' and 'limit' parameters from the query parameters
        user_id = request.query_params.get('user', None)
        limit = request.query_params.get('limit', None)

        # Initialize the queryset with all notifications
        queryset = Notification.objects.all()

        # Filter notifications based on the 'user' parameter
        if user_id:
            # Validate user ID
            if not user_id.isdigit():
                return Response({'error': 'Invalid user ID.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Retrieve the user
                user = User.objects.get(id=user_id)
                queryset = queryset.filter(user=user)
            except User.DoesNotExist:
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Apply the limit if provided
        if limit and limit.isdigit() and int(limit) > 0:
            queryset = queryset.order_by('-created_date')[:int(limit)]

        serializer = NotificationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class UserAdsVisitedCreate(APIView):
    def get(self, request, format=None):
        user_ads_visited = UserAdsVisited.objects.all()
        serializer = UserAdsVisitedSerializer1(user_ads_visited, many=True)
        user_id = request.query_params.get('user')
        limit = request.query_params.get('limit')

        if user_id:
            user_ads_visited = UserAdsVisited.objects.filter(user=user_id)
        else:
            user_ads_visited = UserAdsVisited.objects.all()

        if limit:
            user_ads_visited = user_ads_visited[:int(limit)]
        serializer = UserAdsVisitedSerializer1(user_ads_visited, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        user_id = request.data.get('user')
        ad_id = request.data.get('ad')

        # Check if a similar entry already exists
        existing_entry = UserAdsVisited.objects.filter(user=user_id, ad=ad_id).first()

        if existing_entry:
            # If entry already exists, return a response indicating duplication
            serializer = UserAdsVisitedSerializer(existing_entry)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # If entry does not exist, create a new one
        serializer = UserAdsVisitedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
from django.http import Http404
from django.db.models import Avg

# class SellerReviewListCreateAPIView(APIView):
#     def get(self, request, format=None):
#         seller_id = request.query_params.get('seller_id')
#         if seller_id:
#             reviews = SellerReview.objects.filter(seller_id=seller_id)
#             if not reviews:
#                 raise Http404("No reviews found for the specified seller_id.")
#             avg_rating = reviews.aggregate(Avg('rating_value'))['rating_value__avg']
#             serializer = SellerReviewSerializer(reviews, many=True)
#             data = serializer.data
#             data.append({'average_rating_value': avg_rating})
#             return Response(data)
#         else:
#             reviews = SellerReview.objects.all()
#             serializer = SellerReviewSerializer(reviews, many=True)
#             return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = SellerReviewSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class TopSellerReviewsAPIView(APIView):
#     def get(self, request, format=None):
#         seller_id = request.query_params.get('seller_id')
#         if not seller_id:
#             return Response({"error": "seller_id parameter is required"}, status=400)

#         try:
#             reviews = SellerReview.objects.filter(seller_id=seller_id).order_by('-rating_value')[:10]
#             if not reviews:
#                 raise Http404("No reviews found for the specified seller_id.")
#             serializer = SellerReviewSerializer(reviews, many=True)
#             return Response(serializer.data)
#         except SellerReview.DoesNotExist:
#             raise Http404("Seller does not exist.")
        
