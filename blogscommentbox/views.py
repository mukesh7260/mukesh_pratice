from .models import BlogsComment
from .serializers import BlogsCommentSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from django.core import serializers
from django.http import HttpResponse

class BlogsCommentView(viewsets.ModelViewSet):
    queryset = BlogsComment.objects.all()
    serializer_class = BlogsCommentSerializer   

class blogsComment(APIView):
    def get(self, request, format=None):
        ads=request.get["ads"]
        print("@@ads",ads)
        adsData=BlogsComment.objects.filter(ads =ads)
        qs_json = serializers.serialize('json', adsData)
        return HttpResponse(qs_json, content_type='application/json')    
