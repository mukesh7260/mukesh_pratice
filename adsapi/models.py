from unicodedata import category
from django.db import models
from embed_video.fields import EmbedVideoField
from account.models import User
from jsonfield import JSONField
from picklefield.fields import PickledObjectField
from paymentapi.models import Order
import pytz

# Create your models here.
STATE_CHOICES = (
    ('Andaman & Nicobar Islands','Andaman & Nicobar Islands'),
    ('Andhra Pradesh' , 'Andhra Pradesh'),
    ('Arunachal Pradesh','Arunachal Pradesh'),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('Chandigarh','Chandigarh'),
    ('Chhattisgarh','Chhattisgarh'),
    ('Dadra & Nagar Haveli','Dadra & Nagar Haveli'),
    ('Daman and Diu','Daman and Diu'),
    ('Delhi','Delhi'),
    ('Goa','Goa'),
    ('Gujrat','Gujrat'),
    ('Haryana','Haryana'),
    ('Himachal Pradesh','Himachal Pradesh'),
    ('Jammu & Kashmir','Jammu & Kashmir'),
    ('Jharkhand','Jharkhand'),
    ('Karnataka','Karnataka'),
    ('Kerala','Kerala'),
    ('Lakshadweep','Lakshadweep'),
    ('Madhya Pradesh','Madhya Pradesh'),
    ('Maharastra','Maharastra'),
    ('Manipur','Manipur'),
    ('Meghalaya','Meghalaya'),
    ('Mizoram','Mizoram'),
    ('Nagaland','Nagaland'),
    ('Odisha','Odisha'),
    ('Puducherry','Puducherry'),
    ('Punjab','Punjab'),
    ('Rajasthan','Rajasthan'),
    ('Sikkim','Sikkim'),
    ('Tamil Nadu','Tamil Nadu'),
    ('Telengana','Telengana'),
    ('Tripura','Tripura'),
    ('Uttarkhand','Uttarkhand'),
    ('Uttar Pradesh','Uttar Pradesh'),
    ('West Bengal','West Bengal'),
)
from django.db.models import Q
from datetime import timedelta
from django.dispatch import receiver
from django.utils import timezone
from django.db.models.signals import post_save
from django.urls import reverse


class Product(models.Model):
    CONDITION = (
        ('Excellent', 'Excellent'), 
        ('Good', 'Good'),
        ('Fair', 'Fair'),
    )
    image = models.CharField(max_length=1502222222222222,null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=150,null=False,blank=False)
    price = models.DecimalField(max_digits=11,decimal_places=2,null=True,blank=False)
    tags = models.CharField(max_length=150,null=True,blank=False)
    description = models.TextField()
    # added seller_type as user_type
    seller_type = models.CharField(max_length=100,default="null")
    category = models.CharField(max_length=50,null=True,blank=True)
    brand = models.CharField(max_length=200)
    condition = models.CharField(max_length=100, choices=CONDITION)
    state = models.CharField(default="null", max_length=50)
    City = models.CharField(default="null", max_length=50)
    locality = models.CharField(default="null", max_length=200)
    zip_code = models.CharField(default="null", max_length=6)
    lati = models.CharField(max_length=100,default=0)
    long = models.CharField(max_length=100,default=0)
    video = EmbedVideoField(null=True, blank=True) 
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    subCategoryType=models.CharField(default="null",max_length=3232)
    subCategoryValue=models.CharField(default="null",max_length=3232)
    viewsproduct = models.IntegerField(default=0)
    phoneNumber =models.CharField(default="null",null=True,blank=True,max_length=112)
    BuildUpArea =models.CharField(default="NoData",null=True,blank=True,max_length=112111)
    Flor =models.CharField(default="NoData",null=True,blank=True,max_length=112111)
    ApartMentType =models.CharField(default="NoData",null=True,blank=True,max_length=112111)
    Availability =models.CharField(default="NoData",null=True,blank=True,max_length=112111)
    FurnishedType =models.CharField(default="NoData",null=True,blank=True,max_length=112111)
    Property =models.CharField(default="NoData",null=True,blank=True,max_length=112111)
    Parking =models.CharField(default="NoData",null=True,blank=True,max_length=112111)
    PowerBackup =models.CharField(default="NoData",null=True,blank=True,max_length=112111)
    Gym =models.CharField(default="NoData",null=True,blank=True,max_length=112111)
    Garden =models.CharField(default="NoData",null=True,blank=True,max_length=112111)
    Pool =models.CharField(default="NoData",null=True,blank=True,max_length=112111)
    Lift =models.CharField(default="NoData",null=True,blank=True,max_length=112111)
    PlanCategory = models.CharField(default="null", max_length=2322,null=True)
    featured_ads = models.CharField(default="null", max_length=2322,null=True)
    ads_limit = models.CharField(default="null", max_length=2322,null=True)
    ads_timing = models.CharField(default="null", max_length=2322,null=True)
    top_listing = models.CharField(default="null", max_length=2322,null=True)
    support = models.CharField(default="null", max_length=2322,null=True)
    colorCheck= models.CharField(default="null", max_length=2322,null=True)
    sizeCheck= models.CharField(default="null", max_length=2322,null=True)
    oldPetsCheck= models.CharField(default="null", max_length=2322,null=True)
    start= models.CharField(default="null", max_length=2322,null=True)
    end= models.CharField(default="null", max_length=2322,null=True)
    school=models.CharField(default="null", max_length=2322,null=True)
    college=models.CharField(default="null", max_length=2322,null=True)
    brand=models.CharField(default="null", max_length=2322,null=True)
    engine=models.CharField(default="null", max_length=2322,null=True)
    year=models.CharField(default="null", max_length=2322,null=True)
    kmdriven=models.CharField(default="null", max_length=2322,null=True)
    setkmDriven=models.CharField(default="null", max_length=2322,null=True)
    registrationYear=models.CharField(default="null", max_length=2322,null=True)
    setregistrationYear=models.CharField(default="null", max_length=2322,null=True)
    extraField=models.CharField(max_length=232333332,null=True)
    adsType=models.CharField(default="null", max_length=232333332,null=True)
    plan=models.CharField(default="null", max_length=232333332,null=True)
    expiry=models.BooleanField()
    deleted=models.BooleanField(default=False)
    uuid=models.CharField(default="null", max_length=123123,null=True)
    phoneNumberCollectVisiters=models.CharField(default="null", max_length=123123,null=True)
    
    created_date = models.DateTimeField(default=timezone.now)
    validity = models.PositiveIntegerField(default=2)   
    expiry_date = models.DateTimeField(null=True, blank=True)  
    
   
    def save(self, *args, **kwargs):
        # Check if DaysLimit is set and greater than 0
        if self.validity >= 0:
            # Calculate the expiration date based on the current date and DaysLimit
            current_date = timezone.now()
            expiration_date = self.created_date + timezone.timedelta(minutes=self.validity)
            # Convert the expiration date to a string and store it in date_expire
            self.expiry_date = expiration_date.strftime('%Y-%m-%d %H:%M:%S %z')
        else:
            self.expiry_date = None  # Set date_expire to None if DaysLimit is not set
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
            # Increment the total_ads_posted field of the associated user
            if self.user:
                self.user.total_ads_posted += 1
                self.user.save()

            super().save(*args, **kwargs)
            
    # def generate_qr_code_data(self):
    #     return f"Product-{self.category}-{self.brand}-{self.id}"
    # def generate_qr_code_data(self):
    #     # return "http://example.com/static/product-detail/" + str(self.id) + "/"
    #     return "http://127.0.0.1:8000/api/adsapi/productdetail/" + str(self.id) + "/"
    #     # return "https://databytess.com/api/user/profile/"
    def generate_qr_code_data(self):
        user_info = f"User: {self.user.name}, Phone: {self.user.phoneNumber}"
        return f"{user_info}, Product: {self.title}"
        
    def save(self, *args, **kwargs):
        # Check if the user is specified
        if self.user:
            # Create a notification when a new product is posted
            # message = f"{self.title} product posted successfully."
            message = f"Your Posted {self.title} Post Succesfully."

            Notification.objects.create(user=self.user, message=message)

        super().save(*args, **kwargs)

    
    @classmethod
    def search(cls, search_term):
        return cls.objects.filter(
            Q(title__icontains=search_term) |
            Q(price__icontains=search_term) |
            Q(City__icontains=search_term)
        )

#Wishlist Models
class WishListItems(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,blank=True)
    #wishlist = models.ForeignKey(WishList,on_delete=models.CASCADE, related_name='wishlistitems')
    item = models.ForeignKey(Product, on_delete=models.CASCADE,blank=True, null=True)  


# class AdsMessage(models.Model):
#     userid=models.ForeignKey(User,related_name='related_primary_manual_roats', on_delete=models.CASCADE)
#     adsUserId=models.ForeignKey(User, related_name='related_secondary_manual_roats',on_delete=models.CASCADE)
#     message=models.JSONField()
# class AdsMessagename(models.Model):
#     userid=models.ForeignKey(User,related_name='related_primary_manual_roats', on_delete=models.CASCADE)
#     adsUserId=models.ForeignKey(User, related_name='related_secondary_manual_roats',on_delete=models.CASCADE)
#     message=models.TextField()
import datetime
class adsmangeme(models.Model):
    userid=models.ForeignKey(User,related_name='related_primary_manual_roats', on_delete=models.CASCADE)
    adsUserId=models.ForeignKey(User, related_name='related_secondary_manual_roats',on_delete=models.CASCADE)
    message=models.TextField()
    connectMember=models.CharField(max_length=223232,default="srishtisrija@gmail.com")
    date_created =models.CharField(max_length=20,default=datetime.datetime.now().strftime('%Y-%m-%d'))



class AdsAdressLatLon(models.Model):
    ads=models.ForeignKey(Product, on_delete=models.CASCADE)
    lat=models.IntegerField()
    lon=models.IntegerField()

class ImageAdsModels(models.Model):
    ads= models.ForeignKey(Product, on_delete=models.CASCADE,blank=True, null=True) 
    image=models.CharField(max_length=1502222222222222,null=True,blank=True)

class RealEstateEnquery(models.Model):
    firstName=models.CharField(max_length=232)
    lastName=models.CharField(max_length=232)
    email=models.CharField(max_length=343)
    zip_code=models.CharField(max_length=232)
    date_created = models.CharField(max_length=150,null=False,blank=False ,default=datetime.datetime.now().strftime('%Y-%m-%d'))
    
class ReportAds(models.Model):
    ads= models.ForeignKey(Product, on_delete=models.CASCADE,blank=True, null=True)
    report=models.CharField(max_length=23222)
    dates = models.CharField(max_length=30,default=datetime.datetime.now().strftime('%Y-%m-%d'))
    
     
class AdsComment(models.Model):
    ads= models.ForeignKey(Product, on_delete=models.CASCADE,blank=True, null=True)
    email=models.CharField(max_length=23222)
    datetimeValue=models.CharField(max_length=232)
    message=models.CharField(max_length=23222)
    rating = models.IntegerField(default=0)  # Add rating field as an integer field, defaulting to 0
    def save(self, *args, **kwargs):
        # Check if the notification has already been created
        if hasattr(self, '_notification_created') and self._notification_created:
            super().save(*args, **kwargs)
            return

        # Check if the associated ad and its user exist before creating the notification
        if self.ads and self.ads.user:
            # notification_message = f"Comment posted for {self.ads.title} by {self.email}"
            notification_message = f"{self.email} Commented on Your Post {self.ads.title} and comment as {self.message}"


            # Use update_or_create to ensure only one notification is created for the comment
            notification, created = Notification.objects.update_or_create(
                message=self,
                user=self.ads.user,
                defaults={'message': notification_message}
            )

            # Set the flag to indicate that the notification has been created
            self._notification_created = created

        super().save(*args, **kwargs)
            
            
class LastLogin(models.Model):
    userlogin= models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    lastloginValue =models.CharField(max_length=2322)


class QrCode(models.Model):
    image= models.CharField(default="NoData",null=True,blank=True,max_length=112111)
    product= models.ForeignKey(Product, on_delete=models.CASCADE,blank=True, null=True)
    token = models.CharField(max_length=36,default="null")

class Pricing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=2322,null=True)
    days = models.CharField(max_length=2322,null=True)
    regulars = models.CharField(max_length=2322,null=True)
    # topAds = models.CharField(max_length=2322,null=True)
    featured = models.CharField(max_length=2322,null=True)
    response=models.CharField(max_length=1211,null=True)
    teleSupport = models.BooleanField(default=False)
    chatSupport=models.BooleanField(default=False)
    dedicatedRm=models.BooleanField(default=False)
    hol9Website=models.BooleanField(default=False)
    OrderID=models.CharField(max_length=1211,null=True)
    ads_timing = models.CharField(max_length=30,default=datetime.datetime.now().strftime('%Y-%m-%d'))
    validity= models.CharField(max_length=2322,null=True)

class BusinessPricing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    OrderID=models.CharField(max_length=1211,null=True)
    category = models.CharField(max_length=2322,null=True)
    validity= models.CharField(max_length=2322,null=True)
    city= models.CharField(max_length=2322,null=True)
    visiblity= models.CharField(max_length=2322,null=True)
    NoAds=models.CharField(max_length=2322,null=True)
    teleSupport = models.BooleanField(default=True)
    chatSupport=models.BooleanField(default=True)
    dedicatedRm=models.BooleanField(default=True)
    hol9Website=models.BooleanField(default=True)

#admin auth 
class AdminAuth(models.Model):
    username=models.CharField(max_length=2322,null=False)
    password =models.CharField(max_length=2322,null=False)
    name=models.CharField(max_length=2322,null=True)



class PaymentDetailsValues(models.Model):
    UserValue=models.ForeignKey(User, on_delete=models.CASCADE)
    PlanValue=models.ForeignKey(Pricing, on_delete=models.CASCADE)
    OrderValue=models.ForeignKey(Order, on_delete=models.CASCADE)
    date = models.CharField(max_length=10,blank=False ,default=datetime.datetime.now().strftime('%Y-%m-%d'))
    
class WishlistData(models.Model):
    User=models.ForeignKey(User, on_delete=models.CASCADE)
    wishlistData=models.CharField(max_length=2322,null=False)

class CurrentDate(models.Model):
    dateFiled=models.CharField(max_length=1211)


class BusinessProfile(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    phone_number = models.CharField(max_length=20, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    company_name = models.CharField(max_length=100, blank=False, null=False)
    aadhar_card = models.FileField(upload_to='', blank=False, null=False)
    pan_card = models.FileField(upload_to='', blank=False, null=False)
    company_document = models.FileField(upload_to='', blank=False, null=False)
    # add to live server
    company_document_type = models.TextField(blank=False, null=False, default="null")
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class EmployeeLogin2(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    date = models.CharField(max_length=255,null=True,blank=True)
    login_time = models.CharField(max_length=255,null=True,blank=True)
    longitude1 = models.CharField(max_length=255,null=True,blank=True)
    lattiude1 = models.CharField(max_length=255,null=True,blank=True)
    logout_time = models.CharField(max_length=255,null=True,blank=True)
    longitude2 = models.CharField(max_length=255,null=True,blank=True)
    lattiude2 = models.CharField(max_length=255,null=True,blank=True)
    total_time = models.CharField(max_length=255,null=True,blank=True)


from datetime import datetime
class AssignTask(models.Model):
    assignee_name = models.CharField(max_length=255,null=True,blank=True)
    project_name = models.CharField(max_length=255,null=True,blank=True)
    tl_name = models.CharField(max_length=255,null=True,blank=True)
    task_name = models.CharField(max_length=255,null=True,blank=True)
    due_date  = models.CharField(max_length=255,null=True,blank=True)
    overdue_duedate = models.BooleanField(default=False)
    task_done = models.BooleanField(default=False)
    push_code = models.BooleanField(default=False)
    dev_review = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        if self.due_date:
            due_date_obj = datetime.strptime(self.due_date, '%Y-%m-%d')  # Adjust the format as needed


            if due_date_obj.date() < datetime.now().date():
                self.overdue_duedate = True
            else:
                self.overdue_duedate = False


        super(AssignTask, self).save(*args, **kwargs)


    def __str__(self):
        return self.task_name




class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    message = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)




class Top50Products(models.Model):
    products = models.ManyToManyField('Product')
    
    

class UserAdsVisited(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ad = models.ForeignKey(Product, on_delete=models.CASCADE)
    visited_at = models.DateTimeField(auto_now_add=True)
    
    
    
# class SellerReview(models.Model):
#     seller_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_reviews')
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reviews')
#     date = models.CharField(max_length=100)
#     city = models.CharField(max_length=100)
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     rating_value = models.IntegerField() 
#     comment = models.TextField()