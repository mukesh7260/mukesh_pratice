from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from .views import BlogsView

route = routers.DefaultRouter()
route.register("",BlogsView,basename='blogsview')

urlpatterns = [
    path('',include(route.urls))
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

