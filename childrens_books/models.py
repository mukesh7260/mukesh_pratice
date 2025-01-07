from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


AGE_GROUP_CHOICES = [
    ('0-3', '0-3'),
    ('4-7', '4-7'),
    ('8-12', '8-12'),
]


CATEGORY_CHOICES = [
    ('picture_books', 'Picture Books'),
    ('chapter_books', 'Chapter Books'),
    ('educational_stories', 'Educational Stories'),
    ('activity_books', 'Activity Books'),
]

class BookAd(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    age_group = models.CharField(max_length=5, choices=AGE_GROUP_CHOICES)
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    state = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='children_book/')
    phone_number = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def save(self, *args, **kwargs):
        if BookAd.objects.filter(photo=self.photo).count() >= 12:
            raise ValueError("You can upload only up to 12 photos.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
