from django.shortcuts import render
from .serializers import ToysandGamesSerializer
from .models import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Q

# Create your views here.
class ToysandGamesViews(APIView):
    def post(self,request):
        serializer=ToysandGamesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Ad post Succesfully...!!", status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    # def get(self,request):
    #     user_id=request.query_params.get('user_id')

    #     if user_id:
    #         try:
    #             user=User.objects.get(id=user_id)
    #             ads=ToysandGames.objects.filter(user=user)
    #             serializer=ToysandGamesSerializer(ads,many=True)
    #             return Response(serializer.data, status=status.HTTP_200_OK)
    #         except User.DoesNotExist:
    #             return Response( "User not found.", status=status.HTTP_404_NOT_FOUND)
            
    #     ads = ToysandGames.objects.all()
    #     serializer = ToysandGamesSerializer(ads, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        user_id = request.query_params.get('user_id')
        category = request.query_params.get('category')
        location = request.query_params.get('location')
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        search_query = request.query_params.get('search_query')

        # Start with all Fashion objects
        ads = ToysandGames.objects.all()

        # Filter by user if `user_id` is provided
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                ads = ads.filter(user=user)
            except User.DoesNotExist:
                return Response("User not found.", status=status.HTTP_404_NOT_FOUND)

        # Apply additional filters
        if category:
            ads = ads.filter(category=category)
            
        if location:
            ads = ads.filter(location=location)

        if min_price and max_price:
            ads = ads.filter(price__gte=int(min_price), price__lte=int(max_price))

        if search_query:
            ads = ads.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

        # Serialize the filtered queryset
        serializer = ToysandGamesSerializer(ads, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def put(self,request,ad_id):
        ad=get_object_or_404(ToysandGames,id=ad_id)
        if str(ad.user_id) != str(request.data.get('user_id')):
            return Response("You are not authorized to update this ad.", status=status.HTTP_403_FORBIDDEN)
        
        serializer=ToysandGamesSerializer(ad, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response("Ad Updated Succesfully..!!", status=status.HTTP_200_OK)
        
    def delete(self,request,ad_id):
        ad=get_object_or_404(ToysandGames,id=ad_id)
        if str(ad.user_id) != str(request.data.get('user_id')):
            return Response("You are not authorized to update this ad.", status=status.HTTP_403_FORBIDDEN)
        
        ad.delete()
        return Response(" Advertise deleted..!!",status=status.HTTP_204_NO_CONTENT)


