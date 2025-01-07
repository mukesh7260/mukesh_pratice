from unicodedata import category
from django.db import models
from embed_video.fields import EmbedVideoField
from account.models import User

# Create your models here.
STATE_CHOICES = (
    ('Andaman & Nicobar Islands','Andaman & Nicobar Islands'),
    ('Andhra Pradesh' , 'Andhra Pradesh'),
    ('Arunachal Pradesh','Arunachal Pradesh'),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('Chandigarh','Chandigarh'),
    ('Chhattisgarh','Chhattisgarh'),
    ('Dadra & Nagar Haveli','Dadra & Nagar Haveli'),
    ('Daman and Diu','Daman and Diu'),
    ('Delhi','Delhi'),
    ('Goa','Goa'),
    ('Gujrat','Gujrat'),
    ('Haryana','Haryana'),
    ('Himachal Pradesh','Himachal Pradesh'),
    ('Jammu & Kashmir','Jammu & Kashmir'),
    ('Jharkhand','Jharkhand'),
    ('Karnataka','Karnataka'),
    ('Kerala','Kerala'),
    ('Lakshadweep','Lakshadweep'),
    ('Madhya Pradesh','Madhya Pradesh'),
    ('Maharastra','Maharastra'),
    ('Manipur','Manipur'),
    ('Meghalaya','Meghalaya'),
    ('Mizoram','Mizoram'),
    ('Nagaland','Nagaland'),
    ('Odisha','Odisha'),
    ('Puducherry','Puducherry'),
    ('Punjab','Punjab'),
    ('Rajasthan','Rajasthan'),
    ('Sikkim','Sikkim'),
    ('Tamil Nadu','Tamil Nadu'),
    ('Telengana','Telengana'),
    ('Tripura','Tripura'),
    ('Uttarkhand','Uttarkhand'),
    ('Uttar Pradesh','Uttar Pradesh'),
    ('West Bengal','West Bengal'),
    )



import datetime
class Profile(models.Model):
    image = models.CharField(max_length=62322222222222222,null=False,blank=False,default="null")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=150,null=False,blank=False)
    email = models.CharField(max_length=150,null=False,blank=False)
    PhoneNumber = models.CharField(max_length=25,null=False,blank=False)
    address = models.TextField()
    state = models.CharField(choices=STATE_CHOICES,max_length=50)
    city = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=6,null=False,blank=False)
    date = models.CharField(max_length=10,blank=False ,default=datetime.datetime.now().strftime('%Y-%m-%d'))
    image_base64 = models.TextField(blank=True, null=True)
