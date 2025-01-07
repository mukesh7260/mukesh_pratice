from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(ToysandGames)
class ToysandGamesAdmin(admin.ModelAdmin):
    list_display=('id','ad_title','category','price','location','user')