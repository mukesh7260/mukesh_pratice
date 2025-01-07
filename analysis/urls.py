from django.urls import path
from analysis.views import *

urlpatterns = [
  path('users/',users, name='users'),
  path('blogs/',blogs, name='blogs'),
  path('profile/',profile, name='profile'),
  path('ads/',ads, name='ads'),
  path('pages/',pages, name='pages'),
  path('telemtrydaa/',telemtrydaa, name='telemtrydaa'),
  # path('allPlanData/',allPlanData, name='allPlanData'),





]