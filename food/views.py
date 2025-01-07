from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .models import Foods
from .serializers import FoodSerializer
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


class FoodAPIView(APIView):


    def post(self ,request):
        serializer = FoodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self,request):
        user_id=request.query_params.get('user_id')
  
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                ads = Foods.objects.filter(user=user)
                serializer = FoodSerializer(ads, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response( "User not found.", status=status.HTTP_404_NOT_FOUND)
   
        ads = Foods.objects.all()
        serializer = FoodSerializer(ads, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
       
 
    def put(self,request,ad_id):
        ad = get_object_or_404(Foods, id=ad_id)
 
        if str(ad.user.id) != str(request.data.get('user_id')):
            return Response("You are not authorized to update this ad.", status=status.HTTP_403_FORBIDDEN)
           
        serializer=FoodSerializer(ad,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response("Data Update Succesfully..!!",status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
   
 
   
    def delete(self,request,ad_id):
        ad = get_object_or_404(Foods, id=ad_id)
 
        if str(ad.user.id) != str(request.data.get('user_id')):
            return Response("You are not authorized to update this ad.", status=status.HTTP_403_FORBIDDEN)
       
        ad.delete()
        return Response("Ad deleted successfully.", status=status.HTTP_204_NO_CONTENT)