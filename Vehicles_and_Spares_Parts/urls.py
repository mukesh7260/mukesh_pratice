from django.urls import path
from . views import *



urlpatterns = [
    path('advehicle/',VehicleView.as_view(),name='Vehicles Ads'),
    path('advehicle/<int:ad_id>/',VehicleView.as_view(),name='Vehicles Ads Details'),
    path('adspareparts/',SparePartsView.as_view(),name='Spare Parts Ads'),
    path('adspareparts/<int:ad_id>/',SparePartsView.as_view(),name='Spare Parts Ads Details'),
]