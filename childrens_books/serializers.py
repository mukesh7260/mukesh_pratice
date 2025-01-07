from rest_framework import serializers
from .models import BookAd
from django.contrib.auth import get_user_model

User = get_user_model()

class BookAdSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  

    class Meta:
        model = BookAd
        fields = '__all__'  