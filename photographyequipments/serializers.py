from rest_framework import serializers
from .models import *


class PhotographyEquipmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model=PhotographyEquipments
        fields='__all__'

    def validate_mobile_number(self,value):
        value_str=str(value)
        if len(value_str) != 10:
            raise serializers.ValidationError("Phone number must be exact 10 digit")
        return value