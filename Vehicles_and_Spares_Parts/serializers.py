from rest_framework import serializers
from . models import *




class VehiclesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vehicles
        fields="__all__"



class SparePartsSerializer(serializers.ModelSerializer):
    class Meta:
        model=SpareParts
        fields="__all__"