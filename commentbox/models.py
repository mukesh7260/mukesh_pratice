from django.db import models
from account.models import User
from adsapi.models import Product
# Create your models here.
import datetime
class AdsComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ads = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments',null=False)
    date = models.CharField(max_length=10)
    comment = models.TextField()
    date = models.CharField(max_length=10,blank=False ,default=datetime.datetime.now().strftime('%Y-%m-%d'))


    