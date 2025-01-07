from rest_framework import serializers
from . models import ToysandGames


class ToysandGamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToysandGames
        fields="__all__"

    def validate_phone_number(self,value):
        value_str = str(value)
        if len(value_str) != 10:
            raise serializers.ValidationError("Mobile NUmber must be exactly 10 digit")
        return value
