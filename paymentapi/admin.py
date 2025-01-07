from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Order)
admin.site.register(TransactionDetails)
admin.site.register(Enquiry)
admin.site.register(VerifiedCustomerMain)
# admin.site.register(TransationIdone)