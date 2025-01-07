from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Item(models.Model):
    CATEGORY_CHOICES = [
        ('Books', 'Books'),
        ('Gym & Fitness', 'Gym & Fitness'),
        ('Musical Instruments', 'Musical Instruments'),
        ('Sports Equipment', 'Sports Equipment'),
        ('Other Hobbies', 'Other Hobbies'),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.CharField(max_length=10)
    photo = models.ImageField(upload_to='uploads/')
    location = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def save(self, *args, **kwargs):
        if Item.objects.filter(photo=self.photo).count() >= 12:
            raise ValueError("You can upload only up to 12 photos.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
