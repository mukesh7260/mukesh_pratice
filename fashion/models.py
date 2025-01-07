from django.db import models
from django.contrib.auth import get_user_model
# from . models import User

User = get_user_model()
# Create your models here.

class Fashion(models.Model):
    CATEGORY_CHOICES={
        'Men': 'Men',
        'Women':'Women',
        'Kids' : 'Kids'
    }

    ad_title=models.CharField(max_length=100)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    description=models.TextField()
    images=models.ImageField(upload_to='images/', blank=True, null=True)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ad_title}--{self.category}--{self.price}"