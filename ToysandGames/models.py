from django.db import models
from django.contrib.auth import get_user_model


User=get_user_model()
# Create your models here.

class ToysandGames(models.Model):
    category_choices={
        'Action Figures' : 'Action Figures',
        'Educational Toys' : 'Educational Toys',
        'Board Games' : 'Board Games',
        'Puzzles' : 'Puzzles'
    }

    ad_title=models.CharField(max_length=255)
    description=models.TextField()
    category=models.CharField(max_length=100,choices=category_choices)
    images=models.ImageField(upload_to='images/')
    price=models.DecimalField(max_digits=10, decimal_places=2)
    phone_number=models.IntegerField()
    location=models.CharField(max_length=150)
    state=models.CharField(max_length=150)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ad_title}--{self.category}--{self.price}"
    