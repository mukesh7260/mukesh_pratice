from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import AdsCommentView, adsComment

route = routers.DefaultRouter()
route.register("",AdsCommentView,basename='AdsCommentView')

urlpatterns = [
    path('',include(route.urls)),
    path('adsComment/',adsComment.as_view(),name='adsComment')
]

