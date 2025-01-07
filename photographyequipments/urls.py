from django.urls import path
from .views import *

urlpatterns = [
    path('adpostphoto/',PhotographyEquipmentView.as_view(),name="ad post and get"),
    path('adpostphoto/<int:ad_id>/',PhotographyEquipmentView.as_view(),name="ad put and delete"),
]



