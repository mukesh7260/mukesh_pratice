from django.urls import path
from . views import *



urlpatterns = [
    path('adfashion/',FashionView.as_view(),name='Fashion Ad'),
    path('adfashion/<int:ad_id>/',FashionView.as_view(),name='Fashion Details'),
]
