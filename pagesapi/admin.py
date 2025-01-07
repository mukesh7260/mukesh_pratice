from django.contrib import admin
from .models import Contact
from .models import *

# Register your models here.
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('Name','Email','PhoneNumber','Message')




admin.site.register(SellerReview)
admin.site.register(Traffic)

admin.site.register(NewCustomer)




# ********************************************************************************************************

admin.site.register(Message)
admin.site.register(NotificationMessage)

