from django.urls import path
from .views import *


urlpatterns = [
    path('checkOTP/', checkOTP ),
    path('sendOTP/',otpGeneration),
    path('verifyUserPhone',verifyUserPhone),
    path('sendMessage',sendMessage)
]