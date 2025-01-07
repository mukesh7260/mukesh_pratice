from django.shortcuts import render
from .models import *
from .serializers import FashionSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView


# Create your views here.
class FashionView(APIView):
    def post(self,request):
        serializer=FashionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Ad Post Succesfully...!!",status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    # def get(self,request):
    #     user_id=request.query_params.get('user_id')

    #     if user_id:
    #         try:
    #             user = User.objects.get(id=user_id)
    #             ads = Fashion.objects.filter(user=user)
    #             serializer = FashionSerializer(ads, many=True)
    #             return Response(serializer.data, status=status.HTTP_200_OK)
    #         except User.DoesNotExist:
    #             return Response( "User not found.", status=status.HTTP_404_NOT_FOUND)
    
    #     ads = Fashion.objects.all()
    #     serializer = FashionSerializer(ads, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        user_id = request.query_params.get('user_id')
        category = request.query_params.get('category')
        location = request.query_params.get('location')
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        search_query = request.query_params.get('search_query')

        # Start with all Fashion objects
        queryset = Fashion.objects.all()

        # Filter by user if `user_id` is provided
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                queryset = queryset.filter(user=user)
            except User.DoesNotExist:
                return Response("User not found.", status=status.HTTP_404_NOT_FOUND)

        # Apply additional filters
        if category:
            queryset = queryset.filter(category=category)
            
        if location:
            queryset = queryset.filter(location=location)

        if min_price and max_price:
            queryset = queryset.filter(price__gte=int(min_price), price__lte=int(max_price))

        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

        # Serialize the filtered queryset
        serializer = FashionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def put(self,request,ad_id):
        ad = get_object_or_404(Fashion, id=ad_id)
        if str(ad.user.id) != str(request.data.get('user_id')):
            return Response("You are not authorized to update this ad.", status=status.HTTP_403_FORBIDDEN)
            
        serializer=FashionSerializer(ad,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response("Data Update Succesfully..!!",status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    
    def delete(self,request,ad_id):
        ad = get_object_or_404(Fashion, id=ad_id)
        if str(ad.user.id) != str(request.data.get('user_id')):
            return Response("You are not authorized to update this ad.", status=status.HTTP_403_FORBIDDEN)
        
        ad.delete()
        return Response("Ad deleted successfully.", status=status.HTTP_204_NO_CONTENT)







