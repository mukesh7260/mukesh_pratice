from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Gadgets(models.Model):
    CATEGORY_CHOICES = [
        ('Smartphones', 'Smartphones'),
        ('Tablets & e-Readers', 'Tablets & e-Readers'),
        ('Laptops', 'Laptops'),
        ('Smartwatches', 'Smartwatches'),
        ('Gaming Consoles', 'Gaming Consoles'),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.CharField(max_length=10)
    photo = models.ImageField(upload_to='gadget_uploads/')
    location = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    brand = models.CharField(max_length=255)
    warrenty_avilable = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def save(self, *args, **kwargs):
        if Gadgets.objects.filter(photo=self.photo).count() >= 12:
            raise ValueError("You can upload only up to 12 photos.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
