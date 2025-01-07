from django.urls import path
from .views import *


urlpatterns = [
    path('adfarming/',FarmingandGardeningView.as_view(),name="ad post and get"),
    path('adfarming/<int:ad_id>/',FarmingandGardeningView.as_view(),name="ad put and delete"),
]