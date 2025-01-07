


from rest_framework import serializers
from .models import HealthFitness
from django.contrib.auth import get_user_model

User = get_user_model()

class HealthFitnessSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  

    class Meta:
        model = HealthFitness
        fields = '__all__'  
