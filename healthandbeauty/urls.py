from django.urls import path
from .views import *

urlpatterns = [
    path('adshab/',HealthandBeautyViews.as_view(),name="AD post and get"),
    path('adshab/<int:ad_id>/',HealthandBeautyViews.as_view(),name="AD put and delete"),

]
