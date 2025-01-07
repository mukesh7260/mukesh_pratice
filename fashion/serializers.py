from rest_framework import serializers
from . models import Fashion


class FashionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Fashion
        fields='__all__'