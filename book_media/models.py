from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class BooksMedia(models.Model):
    CATEGORY_CHOICES = [
        ('fiction', 'Fiction & Non-Fiction Books'),
        ('academic', 'Academic Books & Study Materials'),
        ('ebooks', 'E-Books & Audiobooks'),
        ('music', 'Music Instruments & Gear'),
        ('movies', 'Movies & TV Shows (DVDs, Blu-rays)'),
        ('art', 'Art Supplies'),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.CharField(max_length=10)
    photo = models.ImageField(upload_to='bookuploads/',null=True)
    location = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)


    def save(self, *args, **kwargs):
        if BooksMedia.objects.filter(photo=self.photo).count() >= 12:
            raise ValueError("You can upload only up to 12 photos.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
