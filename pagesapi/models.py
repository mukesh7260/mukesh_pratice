from django.db import models
from account.models import *
# Create your models here.
import datetime
class Contact(models.Model):
    Name = models.CharField(max_length=70)
    Email = models.EmailField(max_length=80)
    PhoneNumber = models.IntegerField()
    Message = models.TextField()
    created_at = models.CharField(max_length=150,null=False,blank=False ,default=datetime.datetime.now().strftime('%Y-%m-%d'))




from adsapi.models import Product
class SellerReview(models.Model):
    seller_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_reviews')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    date = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField()
    rating_value = models.IntegerField() 
    comment = models.TextField()
    
    
class Traffic(models.Model):
    name = models.CharField(max_length=200)
    ipconfig = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)  
    email = models.CharField(max_length=15)
    location = models.CharField(max_length=255)
    date = models.CharField(max_length=255)




class NewCustomer(models.Model):
    userid=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    price = models.CharField(max_length=100, blank=True, null=True)
    plan_type = models.CharField(max_length=100, blank=True, null=True)
    validity=models.CharField(max_length=100, blank=True, null=True)
    OrderID=models.CharField(max_length=100, blank=True, null=True)
    ads_count = models.IntegerField(default=0)
    total_count = models.IntegerField(default=0)
    remaining_ads = models.IntegerField(default=0)  # New field to store remaining ads count
    




# ********************************************************************************************************


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    multimedia = models.FileField(upload_to='multimedia/', null=True, blank=True)
    is_system_message = models.BooleanField(default=False)

class NotificationMessage(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)