


from rest_framework import serializers
from .models import Item
from django.contrib.auth import get_user_model

User = get_user_model()

class ItemSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  

    class Meta:
        model = Item
        fields = '__all__'  
