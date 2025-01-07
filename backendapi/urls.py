from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from adsapi.views import AddtoWishListItemsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('account.urls')),
    path('api/',include('pagesapi.urls')),
    path('api/adsapi/',include('adsapi.urls')),
    path('api/blogsapi/',include('blogsapi.urls')),
    path('api/profileapi/',include('profileapi.urls')),
    # path('api/openMoney/',include('opneMoney.urls')),
    #Social oauth URLS
    #Phone Login
    path('api/phone/',include('otp_reg.urls')),
    #WishList URLS
    path('addwishlistitems/<int:pk>', AddtoWishListItemsView.as_view(),name='add-to-wishlist'),
    #AdsComments URLS
    path('api/comment/',include('commentbox.urls')),
    #BlogsComments URLS
    path('api/blogscomment/',include('blogscommentbox.urls')),
    #Payment API
    path('api/payment/',include('paymentapi.urls')),
    # path('api/payu/', include('payu_app.urls')),

#<<<<<<< HEAD
    path('api/hobby/',include('hobby.urls')),
    path('api/food/',include('food.urls')),
    path('api/health/',include('health.urls')),
    path('api/book_media/',include('book_media.urls')),
    path('api/science_technology/',include('science_technology.urls')),
    path('api/childrens_books/',include('childrens_books.urls')),
    path('api/gadgets/',include('gadgets.urls')),
    path('api/farmingandgardening/',include('farmingandgardening.urls')),
    path('api/vehicles/',include('Vehicles_and_Spares_Parts.urls')),
    path('api/toysandgames/',include('ToysandGames.urls')),
    path('api/photographyequipments/',include('photographyequipments.urls')),
    path('api/healthandbeauty/',include('healthandbeauty.urls')),
    path('api/fashion/',include('fashion.urls')),


#=======
<<<<<<< HEAD
    #path('hobby/',include('hobby.urls')),
    #path('food/',include('food.urls')),
    #path('health/',include('health.urls')),
    #path('book_media/',include('book_media.urls')),
    #path('science_technology/',include('science_technology.urls')),
    #path('childrens_books/',include('childrens_books.urls')),
    #path('gadgets/',include('gadgets.urls')),
=======
    path('hobby/',include('hobby.urls')),
    path('food/',include('food.urls')),
    path('health/',include('health.urls')),
    path('book_media/',include('book_media.urls')),
    path('science_technology/',include('science_technology.urls')),
    path('childrens_books/',include('childrens_books.urls')),
    path('gadgets/',include('gadgets.urls')),
>>>>>>> 8a72e49cd22e840587db7c1423cb1ca18330101d
#>>>>>>> 926376c (server side commite)
    

]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
