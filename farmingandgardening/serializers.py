from rest_framework import serializers
from .models import *



class FarmingandGardeningSerializer(serializers.ModelSerializer):
    class Meta:
        model=FarmingandGardening
        fields='__all__'

    def validate_mobile_numner(self,value):
        value_str=str(value)
        if len(value_str) != 10:
            raise serializers.ValidationError("Phone number must be exact 10 digit")
        return value
        
    # def validate_images(self,value):
    #     if len(value) > 15:
    #        raise serializers.ValidationError("You can upload upto 15 images")
    #     for img in value:
    #         if img.size > 5 * 1024 * 1024 :
    #           raise serializers.ValidationError(f"File {img.name} exceeds the 5MB size limit.")
    #     return value
            