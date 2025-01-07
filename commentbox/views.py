from .models import AdsComment
from .serializers import AdsCommentSerializer
from rest_framework import viewsets
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from adsapi.models import Product
from django.core import serializers

class AdsCommentView(viewsets.ModelViewSet):
    queryset = AdsComment.objects.all()
    serializer_class = AdsCommentSerializer  

class adsComment(APIView):
    def get(self, request, format=None):
        ads=request.get["ads"]
        print("@@ads",ads)
        adsData=AdsComment.objects.filter(ads =ads)
        qs_json = serializers.serialize('json', adsData)
        return HttpResponse(qs_json , content_type='application/json')

