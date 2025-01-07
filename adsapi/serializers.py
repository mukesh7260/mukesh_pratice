from rest_framework import serializers
from .models import  Product , WishListItems,BusinessProfile
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def update(self, instance, validated_data):
        # Handle partial updates
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance



class QrCodeSerializer(serializers.Serializer):
    qr_code = serializers.CharField()

 #Wishlist Serializers

class WishListItemsTestSerializer(serializers.ModelSerializer):    
    class Meta:
        model = WishListItems
        fields = ['id','item']
        depth = 2  


class BusinessProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProfile
        fields = '__all__'
    def update(self, instance, validated_data):
        # Handle partial updates
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
    
    
class EmployeeLogin2Serializer2(serializers.ModelSerializer):
    class Meta:
        model = EmployeeLogin2
        fields = '__all__'

class AssignTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignTask
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        

class UserAdsVisitedSerializer1(serializers.ModelSerializer):
    ad_details = ProductSerializer(source='ad', read_only=True)

    class Meta:
        model = UserAdsVisited
        fields = ('id', 'user', 'ad', 'ad_details')
        
class UserAdsVisitedSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAdsVisited
        fields = '__all__'

# class SellerReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SellerReview
#         fields = '__all__'



