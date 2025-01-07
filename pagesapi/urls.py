from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import *

# route = routers.DefaultRouter()
# route.register("",ContactView,basename='contactview')

urlpatterns = [
    # path('',include(route.urls)),
    path('contactus/', ContactView.as_view(), name='contactus'),
    path('contactus/<int:pk>/', ContactViewDetail.as_view(), name='contactus'),
    path('sellerreviews/', SellerReviewListCreateAPIView.as_view(), name='review-list'),
    path('top-seller-reviews/', TopSellerReviewsAPIView.as_view(), name='top-seller-reviews'),
    path('userslist/', UserAPIView.as_view(), name='user_api'),
    path('userslist/<int:pk>/', UserDetailView.as_view(), name='user_detail_api'),
    path('traffic/', TrafficList.as_view(), name='traffic-list'),
    
    path('newuserplan/',NewUserPlanView.as_view(),name='newuserplan'),


# ********************************************************************************************************

    path('send-message/', SendMessageAPIView.as_view(), name='send-message'),
    path('receive-message/', ReceiveMessageAPIView.as_view(), name='receive-message'),
    path('conversation/<int:user_id>/', ConversationAPIView.as_view(), name='conversation'),
    path('notifications/', NotificationListAPIView.as_view(), name='notification-list'),
    path('edit-message/<int:pk>/', EditMessageAPIView.as_view(), name='edit-message'),

    path('alladscommentsavg/', AdsCommentListView.as_view(), name='alladscommentsavg'),

]

