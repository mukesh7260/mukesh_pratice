from django.urls import path
from .views import HealthFitnessListCreateView



urlpatterns = [
    path('health&fitness/',HealthFitnessListCreateView.as_view(),name='health&fitness Ad'),
    path('health&fitness/<int:ad_id>/',HealthFitnessListCreateView.as_view(),name='health&fitness Details'),
]