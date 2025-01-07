from django.contrib import admin
from .models import *

# Register your models here.
# @admin.register(HealthandBeauty)
# class HealthandBeautyAdmin(admin.ModelAdmin):
#     list_display=['ad_title','description','images','price','location','state','phone_number','user']


@admin.register(HealthandBeauty)
class HealthandBeautyAdmin(admin.ModelAdmin):
    list_display = [field.name for field in HealthandBeauty._meta.fields]