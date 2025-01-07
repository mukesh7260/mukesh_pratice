from rest_framework import serializers
from .models import AdsComment

class AdsCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdsComment
        fields = '__all__'
  
