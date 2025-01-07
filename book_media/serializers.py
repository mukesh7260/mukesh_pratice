from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class BooksMediaSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  

    class Meta:
        model = BooksMedia
        fields = '__all__'  
