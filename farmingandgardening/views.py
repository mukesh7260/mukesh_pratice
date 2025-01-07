from django.shortcuts import render,get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from . models import *
from django.db.models import Q
from rest_framework.response import Response

# Create your views here.

class FarmingandGardeningView(APIView):
    def post(self,request):
        serializer=FarmingandGardeningSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Advertise Post Successfully...!!",status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    def get(self,request):
        user_id=request.query_params.get('user_id')
        category = request.query_params.get('category')
        location = request.query_params.get('location')
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        search_query = request.query_params.get('search_query')

        ads = FarmingandGardening.objects.all()

        if user_id:
            try:
                user = User.objects.get(id=user_id)
                ads = ads.filter(user=user)
            except User.DoesNotExist:
                return Response("User not found.", status=status.HTTP_404_NOT_FOUND)
               
        if category:
            ads = ads.filter(category=category)
            
        if location:
            ads = ads.filter(location=location)

        if min_price and max_price:
            ads = ads.filter(price__gte=int(min_price), price__lte=int(max_price))

        if search_query:
            ads = ads.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

        # Serialize the filtered queryset
        serializer = FarmingandGardeningSerializer(ads,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

    def put(self,request,ad_id):
        ad=get_object_or_404(FarmingandGardening, id=ad_id)
        if str(ad.user.id) != str(request.data.get('user_id')):
            return Response("you are not authorized tu update this Advertise ",status=status.HTTP_403_FORBIDDEN)
        serializer=FarmingandGardeningSerializer(ad,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(" Advertise Updated..!!",status=status.HTTP_200_OK)
        return Response(serializer.errors)

    def delete(self,request,ad_id):
        ad=get_object_or_404(FarmingandGardening,id=ad_id)
        if str(ad.user_id) != str(request.data.get('user_id')):
            return Response("you are not authorized tu update this Advertise",status=status.HTTP_403_FORBIDDEN)
        ad.delete()
        return Response("Advertise deleted...!!",status=status.HTTP_204_NO_CONTENT)