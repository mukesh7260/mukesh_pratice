


from rest_framework import serializers
from .models import Gadgets
from django.contrib.auth import get_user_model

User = get_user_model()

class GadgetsSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  

    class Meta:
        model = Gadgets
        fields = '__all__'  