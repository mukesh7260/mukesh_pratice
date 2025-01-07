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
class Blogs(models.Model):
    image = models.ImageField(upload_to ='upload/images',null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    category = models.CharField(max_length=150,null=True,blank=True)
    title = models.CharField(max_length=150,null=False,blank=False)
    description = models.TextField()
    state = models.CharField(choices=STATE_CHOICES,max_length=50)
    city = models.CharField(max_length=50)
    author=models.CharField(max_length=150,null=False,blank=False,default="null")
    published_time=models.CharField(max_length=150,null=False,blank=False ,default="null")
    subtitle=models.CharField(max_length=150,null=False,blank=False,default="null")
    imagesecond= models.ImageField(upload_to ='upload/images',null=False,blank=False,default="null")
    published_time=models.CharField(max_length=150,null=False,blank=False ,default=datetime.datetime.now().strftime('%Y-%m-%d'))
    video = models.FileField(upload_to='video/',null=True,blank=True)
    video_base64 = models.TextField(blank=True,null=True)

class BlogComment(models.Model):
    ads= models.ForeignKey(Blogs, on_delete=models.CASCADE,blank=True, null=True)
    email=models.CharField(max_length=23222)
    datetimeValue=models.CharField(max_length=232)
    message=models.CharField(max_length=23222)
    published_time=models.CharField(max_length=232,blank=False ,default=datetime.datetime.now().strftime('%Y-%m-%d'))
