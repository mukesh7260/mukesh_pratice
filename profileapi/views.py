from django.shortcuts import render
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
# Create your views here.
from django.http import HttpResponse

class ProfileView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer




