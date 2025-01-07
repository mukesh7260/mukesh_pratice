from django.urls import path
from .views import FoodAPIView



urlpatterns = [
    path('food/',FoodAPIView.as_view(),name='food Ad'),
    path('food/<int:ad_id>/',FoodAPIView.as_view(),name='food Details'),
]