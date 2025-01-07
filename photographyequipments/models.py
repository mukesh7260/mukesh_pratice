from django.db import models
from django.contrib.auth import get_user_model

User=get_user_model()

# Create your models here.

class PhotographyEquipments(models.Model):
    category_choices=[
        ('Cameras','Cameras'),
        ('Lenses','Lenses'),
        ('Tripods','Tripods'),
        ('Accessories','Accessories'),
    ]

    condition_choice=[
        ('New','New'),
        ('Used','Used'),
    ]

    product_name=models.CharField(max_length=150)
    category=models.CharField(max_length=150,choices=category_choices)
    brand=models.CharField(max_length=150)
    model=models.CharField(max_length=150)
    condition=models.CharField(max_length=150,choices=condition_choice)
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    photos=models.ImageField(upload_to='images/')
    phone_number=models.CharField(max_length=15)
    location = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product_name} -- {self.category} -- {self.brand} -- {self.model} -- {self.price} -- {self.location} -- {self.phone_number}'



