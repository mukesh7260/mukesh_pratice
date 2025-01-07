from django.urls import path
from .views import ItemAPIView



urlpatterns = [
    path('items/',ItemAPIView.as_view(),name='items Ad'),
    path('items/<int:ad_id>/',ItemAPIView.as_view(),name='items Details'),
]