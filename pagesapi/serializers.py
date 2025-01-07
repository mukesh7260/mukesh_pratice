from rest_framework import serializers
from .models import *

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
  
class SellerReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerReview
        fields = '__all__'
        

class UserSerializerNew(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
        
class TrafficSerializer(serializers.ModelSerializer):
    class Meta:
        model = Traffic
        fields = '__all__'
        


# ********************************************************************************************************


      
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp','multimedia']
        read_only_fields = ['sender', 'timestamp']

    def validate(self, data):
        sender = self.context['request'].user
        data['sender'] = sender
        return data
    
class NotificationMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationMessage
        fields = ['id', 'receiver', 'content', 'timestamp']
        read_only_fields = ['receiver', 'content', 'timestamp']
        

        
from adsapi.models import *      
class AdsCommentSeri(serializers.ModelSerializer):
    class Meta:
        model = AdsComment
        fields = '__all__'