from django.db import models
from django.contrib.auth import get_user_model

User=get_user_model()

# Create your models here.

class FarmingandGardening(models.Model):
    category_choices=[
        ('Farm Equipment','Farm Equipment'),
        ('Plants & Seeds','Plants & Seeds'),
        ('Gardening Tools','Gardening Tools'),
        ('Livestock','Livestock'),
        ('Organic Produce','Organic Produce'),
    ]
    ad_title=models.CharField(max_length=150)
    description=models.TextField()
    category=models.CharField(max_length=150,choices=category_choices)
    images=models.ImageField(upload_to='images/')
    price=models.DecimalField(max_digits=10,decimal_places=2)
    location = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.ad_title} -- {self.category} -- {self.price} -- {self.location} -- {self.phone_number}'
