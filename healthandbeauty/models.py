from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class HealthandBeauty(models.Model):
    CATEGORY_CHOICES = [
        ('Skincare', 'Skincare Products'),
        ('Haircare', 'Haircare Products'),
        ('Makeup', 'Makeup & Cosmetics'),
        ('Personal Care', 'Personal Care Appliances'),
        ('Fitness', 'Fitness Equipment'),
        ('Supplements', 'Supplements & Vitamins'),
    ]

    ad_title = models.CharField(max_length=150)
    description = models.TextField()
    category = models.CharField(max_length=150, choices=CATEGORY_CHOICES)
    images = models.ImageField(upload_to='images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15)  # Use CharField for phone numbers
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.ad_title} -- {self.price} -- {self.location} -- {self.phone_number}'
