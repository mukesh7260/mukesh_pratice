from django.urls import path
from .views import ScienceandTEchAPIView



urlpatterns = [
    path('scienceandtech/',ScienceandTEchAPIView.as_view(),name='scienceandtech Ad'),
    path('scienceandtech/<int:ad_id>/',ScienceandTEchAPIView.as_view(),name='scienceandtech Details'),
]