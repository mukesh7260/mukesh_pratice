from django.urls import path
from .views import BookAdListCreateView



urlpatterns = [
    path('childerns_book/',BookAdListCreateView.as_view(),name='childerns_book Ad'),
    path('childerns_book/<int:ad_id>/',BookAdListCreateView.as_view(),name='childerns_book Details'),
]