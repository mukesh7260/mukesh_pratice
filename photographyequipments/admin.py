from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(PhotographyEquipments)
class PhotographyEquipmentsAdmin(admin.ModelAdmin):
    list_display=('id','product_name','category','brand', 'condition','price','location','user')