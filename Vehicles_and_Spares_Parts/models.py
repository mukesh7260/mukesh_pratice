from django.db import models
from django.contrib.auth import get_user_model

User=get_user_model()

# Create your models here.

class Vehicles(models.Model):
    CATEGORY_CHOICES={
    "Auto-rickshaws & E-rickshaws" : "Auto-rickshaws & E-rickshaws",
    "Buses":"Buses",
    "Trucks":"Trucks",
    "Pick-up vans":"Pick-up vans",
    "Pick-up trucks":"Pick-up trucks",
    "Heavy Machinery":"Heavy Machinery",
    "Scrap Cars":"Scrap Cars",
    "Others":"Others"
    }

    type=models.CharField(max_length=100,choices=CATEGORY_CHOICES)
    year=models.CharField(max_length=120)
    km_driven=models.DecimalField(max_digits=10,decimal_places=4)
    ad_title=models.CharField(max_length=150)
    description=models.TextField()
    images=models.ImageField(upload_to='images/',null=False)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ad_title}--{self.type}--{self.price}"




class SpareParts(models.Model):
    CATEGORY_CHOICES={
    "Wheels & Tyres" : "Wheels & Tyres",
    "Audio & Other":"Audio & Other",
    "Other Spare Parts":"Other Spare Parts"
    }

    type=models.CharField(max_length=100,choices=CATEGORY_CHOICES)
    ad_title=models.CharField(max_length=150)
    description=models.TextField()
    images=models.ImageField(upload_to='images/',null=False)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ad_title}--{self.type}--{self.price}"