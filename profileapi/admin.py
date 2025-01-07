from django.contrib import admin
from .models import Profile
# Register your models here.
@admin.register(Profile)
class Product(admin.ModelAdmin):
    list_display = ('name','email','address','state','city','zipcode')
