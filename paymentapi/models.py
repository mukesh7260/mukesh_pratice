from django.db import models
from account.models import User
import datetime



class TransationIdone(models.Model):
    id1=models.CharField(max_length=2322)
    dateid=models.CharField(max_length=232)
    message=models.CharField(max_length=232)
    # adsid=models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    userid=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    ProductData=models.CharField(max_length=43343333,null=True)
    date_created=models.CharField(max_length=550, default=datetime.datetime.now().strftime('%Y-%m-%d'))

class Order(models.Model):
    order_product = models.CharField(max_length=100)
    order_amount = models.CharField(max_length=25)
    order_payment_id = models.CharField(max_length=100)
    isPaid = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now=True)
    user_email=models.CharField(max_length=150,null=False,blank=False ,default="null")
    product_name=models.CharField(max_length=1530,null=False,blank=False ,default="null")
    order_dateTele = models.CharField(max_length=155,default=datetime.datetime.now().strftime('%Y-%m-%d'))
    
    def __str__(self):
        return self.order_product 

class Transaction(models.Model):
    # Transaction id sent by merchant.
    transaction_id = models.CharField(max_length=100)

    # Payment gateway type used in transaction
    payment_gateway_type = models.CharField(max_length=20, null=True, blank=True)  # Map to PG_TYPE

    # Map to addedon
    transaction_date_time = models.DateTimeField(null=True, blank=True)

    # mode  (credit card/ CD - Cheque / Net Banking)
    mode = models.CharField(max_length=10, null=True, blank=True)
    status = models.CharField(max_length=15, null=True, blank=True)
    amount = models.DecimalField(max_digits=19, decimal_places=6)

    # Unique id from PayU.in
    mihpayid = models.CharField(max_length=100, null=True, blank=True)
    bankcode = models.CharField(max_length=10, null=True, blank=True)

    # Reference number for the payment gateway (received in PG_TYPE)
    bank_ref_num = models.CharField(max_length=100, null=True, blank=True)
    discount = models.DecimalField(max_digits=19, decimal_places=6, default=0)
    additional_charges = models.DecimalField(max_digits=19, decimal_places=6, default=0)  # Charged by Payu

    # Status of transaction in PayU system
    # Map to unmappedstatus(initiated/ in progress /dropped / bounced / captured / auth/ failed / usercancelled/ pending)
    txn_status_on_payu = models.CharField(max_length=20, null=True, blank=True)
    hash_status = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        app_label = 'payu'


class CancelRefundCaptureRequests(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)

    # PayU Request ID for a request in a Transaction.
    request_id = models.CharField(max_length=100)

    # Cancel or Refund or Capture Request
    request_type = models.CharField(max_length=20)

    # Status of webservice call
    status = models.CharField(max_length=15)
    message = models.CharField(max_length=100)

    # PayU ID
    mihpayid = models.CharField(max_length=100)

    # Bank Reference Number
    bank_ref_num = models.CharField(max_length=100, null=True, blank=True)

    amount = models.DecimalField(max_digits=19, decimal_places=6, default=0)
    error_code = models.CharField(max_length=10)

    class Meta:
        app_label = 'payu'

import adsapi.models
class TransactionDetails(models.Model):
    payment_token_id=models.CharField(max_length=100, null=True, blank=True)
    payment_id=models.CharField(max_length=100, null=True, blank=True)
    userID=models.ForeignKey(User, on_delete=models.CASCADE)
    plan=models.CharField(max_length=100, null=True, blank=True)
    paymentStatus=models.CharField(max_length=100, null=True, blank=True)
    email=models.CharField(max_length=100, null=True, blank=True)
    tranid=models.CharField(max_length=100, null=True, blank=True)
    order_payment_amount=models.CharField(max_length=100, null=True, blank=True)
    phoneNumber=models.CharField(max_length=100, null=True, blank=True)
    ordrDate = models.CharField(max_length=155,default=datetime.datetime.now().strftime('%Y-%m-%d'))
    adsValue=models.CharField(max_length=100, null=True, blank=True)
    monthsVale=models.CharField(max_length=100, null=True, blank=True)
    City=models.CharField(max_length=100, null=True, blank=True)
   
    def save(self, *args, **kwargs):
        # Check if the user is specified
        # if self.userID:
        if self.paymentStatus == "Success":
            # Create a notification when a new product is posted
            # message = f"{self.paymentStatus} product posted successfully."
            message = f"Your Purchased {self.plan} Plan"

            adsapi.models.Notification.objects.create(user=self.userID, message=message)

        super().save(*args, **kwargs) 
 

class Enquiry(models.Model):
    CATEGORY_CHOICES = [
        ('real_estate', 'Real Estate'),
        ('furniture', 'Furniture'),
        ('pets', 'Pets'),
        ('bikes', 'Bikes'),
        ('cars', 'Cars'),
        ('electronics', 'Electronics'),
        ('mobiles', 'Mobiles'),
        ('services', 'Services'),
    ]
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    phone_number = models.CharField(max_length=10, blank=False, null=False)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=False, null=False)
    subject =models.TextField(blank=False, null=False)
    description = models.TextField(blank=False, null=False)

    def _str_(self):
        return self.subject


class VerifiedCustomer(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    paymentMoney=models.CharField(max_length=10, blank=False, null=False)

class VerifiedCustomerMain(models.Model):
    userid=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    price = models.CharField(max_length=100, blank=True, null=True)
    plan_type = models.CharField(max_length=100, blank=True, null=True)
    validity=models.CharField(max_length=100, blank=True, null=True)
    OrderID=models.CharField(max_length=100, blank=True, null=True)