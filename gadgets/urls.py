from django.urls import path
from .views import GadgetsAPIView



urlpatterns = [
    path('gadget/',GadgetsAPIView.as_view(),name='gadget Ad'),
    path('gadget/<int:ad_id>/',GadgetsAPIView.as_view(),name='gadget Details'),
]