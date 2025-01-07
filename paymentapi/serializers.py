from rest_framework import serializers
from .models import *


class OrderSerializer(serializers.ModelSerializer):
    order_date = serializers.DateTimeField(format="%d %B %Y %I : %M %p")
    class Meta:
        model = Order
        fields = '__all__'
        depth = 2
        
class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = '__all__'
        
class TransactionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionDetails
        fields = '__all__'