from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Product)
class Product(admin.ModelAdmin):
    list_display = ('id','title','price','tags','brand','condition','state')
admin.site.register(ImageAdsModels)
admin.site.register(LastLogin)
admin.site.register(QrCode)
admin.site.register(Pricing)
admin.site.register(PaymentDetailsValues)
admin.site.register(WishlistData)
admin.site.register(CurrentDate)
admin.site.register(BusinessPricing)
admin.site.register(BusinessProfile)
admin.site.register(EmployeeLogin2)
admin.site.register(AssignTask)
admin.site.register(AdsComment)
admin.site.register(Notification)
admin.site.register(Top50Products)
admin.site.register(UserAdsVisited)

# admin.site.register(SellerReview)



