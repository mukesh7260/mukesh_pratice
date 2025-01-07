from django.urls import path
from django.conf.urls import include
from rest_framework import routers


from .views import BlogsCommentView , blogsComment

route = routers.DefaultRouter()
route.register("",BlogsCommentView,basename='BlogsCommentView')

urlpatterns = [
    path('',include(route.urls)),
    path('blogsComment/',blogsComment.as_view(),name='blogsComment')
]

