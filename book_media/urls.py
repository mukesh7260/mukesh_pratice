from django.urls import path
from .views import BooksMediaAPIView



urlpatterns = [
    path('booksmedia/',BooksMediaAPIView.as_view(),name='booksmedia Ad'),
    path('booksmedia/<int:ad_id>/',BooksMediaAPIView.as_view(),name='booksmedia Details'),
]