from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from .views import *
route = routers.DefaultRouter()
route.register("",ProductView,basename='productview')
# sudo fuser -k 8000/tcp
urlpatterns = [
    path('',include(route.urls)),
    #WishList URLS
    path('productdetail/<int:pk>/', ProductDetail.as_view(), name='productdetail'),
    path('qrcode', generate_qr_code, name='qrcode'),
    path('api/addwishlistitems/<int:pk>', AddtoWishListItemsView.as_view(),name='add-to-wishlist'),
    path('AdsMessage', AdsMessageName.as_view(),name='add-to-message'),
    path('AdsAdressLatLon', AdsAdressLatLonView.as_view(),name='add-to-address'),
    path('chatMessages', chatMessages.as_view(),name='add-to-ChatMessage'),
    path('chatting', chatting.as_view(),name='add-to-chatting'),
    path('uploadImages', uploadImages.as_view(),name='add-to-uploadImages'),
    path('RealEstateEnquery', RealEstateEnquery1.as_view(),name='add-to-RealEstateEnquery'),
    path('ReportAds', ReportAds1.as_view(),name='add-to-ReportAds'),
    path('adsUpload', AdsUpload.as_view(),name='add-to-adsUpload'),
    path('adsCommentBox', adsCommentBoxView.as_view(),name='add-to-adsCommentBox'),
    
    path('blogCommentBox', blogCommentBoxView.as_view(),name='add-to-blogCommentBox'),
    path('qrCodeAds1', QrCodeAds.as_view(),name='add-to-qrCodeAds'),
    path('pricing', PricingViews.as_view(),name='Pricing'),
    path('getPricingViews', getPricingViews.as_view(),name='getPricingViews'),
    path('updatePlanLimit', updatePlanLimit.as_view(),name='updatePlanLimit'),
    ###api to create here 
    path('UserDataCount', UserDataCount.as_view(),name='UserDataCount'),
    path('allAdsByInerval', allAdsByInerval.as_view(),name='allAdsByInerval'),
    path('categoryAdsByInterval', categoryAdsByInterval.as_view(),name='categoryAdsByInterval'),
    path('subCategoryAdsByInterva', subCategoryAdsByInterva.as_view(),name='subCategoryAdsByInterva'),
    path('adminAuth', adminAuth.as_view(),name='adminAuth'),
    path('webCountData', webCountData.as_view(),name='webCountData'),
    path('featuredAdsData', featuredAdsData.as_view(),name='featuredAdsData'),
    path('webCountAsperDate',webCountAsperDate.as_view(),name='webCountAsperDate'),
    path('webCountasPerDateData',webCountasPerDateData.as_view(),name='webCountasPerDateData'),
    path('webCountUSERPerDateData',webCountUSERPerDateData.as_view(),name='webCountUSERPerDateData'),
    path('webCountBLOGSPerDateData',webCountBLOGSPerDateData.as_view(),name='webCountBLOGSPerDateData'),
    path('dataCuntMultipleValues',dataCuntMultipleValues.as_view(),name='dataCuntMultipleValues'),
    path('AdsDataFilter',AdsDataFilter.as_view(),name='AdsDataFilter'),
    path('allPlanData',allPlanData.as_view(), name='allPlanData'),
    path('wishlistData',wishlistData.as_view(), name='wishlistData'),
    path('allPricingPlanData',allPricingPlanData.as_view(), name='allPricingPlanData'),
    path('getExtraCat',getExtraCat.as_view(), name='getExtraCat'),
    path('jobEveryDAYRun',jobEveryDAYRun, name='jobEveryDAYRun'),
    path('webpopuplist',webpopuplist.as_view(),name='webpopuplist'),
    path('DeletedAds',DeletedAds.as_view(),name='DeletedAds'),
    path('searchData',searchData.as_view(),name='searchData'),
    path('approveAds',approveAds.as_view(),name='approveAds'),
    path('SearchAdsWithSort',SearchAdsWithSort.as_view(),name='SearchAdsWithSort'),
    path('SearchWeb',SearchWeb.as_view(),name='SearchWeb'),
    path('checkBusinessPlan',CheckBusinessPlan.as_view(),name='checkBusinessPlan'),
    path('businessAds',BusinessAds.as_view(),name='businessAds'),
    # path('businessProfile', BusinessProfiles.as_view(), name='businessProfile'),
    path('businessProfile', BusinessProfiles.as_view({'get': 'list', 'post': 'create'}), name='businessProfile'),
    path('businessProfileDetail/<int:pk>/', BusinessProfileDetail.as_view(), name='businessProfileDetail'),
    
    path('mybusinessPlan', MybusinessPlan.as_view(), name='mybusinessPlan'),
    path('checkVerified', CheckVerified.as_view(), name='checkVerified'),
    path('collectVisitPhoneNumber', CollectVisitPhoneNumber.as_view(), name='collectVisitPhoneNumber'),
    path('businessProfileVerified', BusinessVerifiedAPI.as_view(), name='businessProfileVerified'),

    path('employeelogin2',EmployeeLoginView2.as_view(), name='employeelogin2'),
    path('employeelogin2/<int:pk>',EmployeeLoginUpdateDelete2.as_view(), name='employeelogin2'),
    path('assigntaskview',AssignTaskView.as_view(), name='assigntaskview'),
    path('assigntaskview/<int:pk>',AssignTaskUpdateDelete.as_view(), name='assigntaskview'),
    
    path('topsellers',TopSellerAdsView.as_view(), name='topsellers'),
    path('trendingads', TrendingAds.as_view(),name='trendingads'),
    
    path('notifications', NotificationAPIView.as_view(), name='notifications'),
    
    path('useradsvisited', UserAdsVisitedCreate.as_view(), name='useradsvisited'),

    # path('sellerreviews/', SellerReviewListCreateAPIView.as_view(), name='review-list'),
    
    # path('top-seller-reviews/', TopSellerReviewsAPIView.as_view(), name='top-seller-reviews'),





]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

