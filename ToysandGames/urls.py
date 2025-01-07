from django.urls import path
from .views import ToysandGamesViews


urlpatterns = [
    path('adtoysandgames/',ToysandGamesViews.as_view(),name='Toys & Games Ad'),
    path('adtoysandgames/<int:ad_id>/',ToysandGamesViews.as_view(),name='Toys & Games Ad'),
]
