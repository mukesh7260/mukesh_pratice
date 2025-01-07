from django.urls import path
from .views import *



urlpatterns = [
    
    # path('pay/',start_payment,name="start_payment"),
    # path('handlepayment/',handlepayment,name="handlepayment"),
    # path('tokenPayment',tokenPayment,name="tokenPayment"),
    #  path('razorpay/pay/', start_payment, name="payment"),
    # path('razorpay/payment/success/', handle_payment_success, name="payment_success"),
    # path('successPaymentData/',SuccessPaymentData.as_view(),name="successPaymentData"),
    # path('generateHashKey', GenerateHashKeyView.as_view(), name="generate-hash"),
    # path('success', SuccessView.as_view(), name="success"),
  
 path('', index, name='Open Layer'),
 
 
	path('callback', callback, name='Open Layer Response'),
    path('create_token', create_payment_token_Class.as_view(), name='create_payment_token'),
    
    
    
    path('userTransData', userTransData.as_view(), name='userTransData'),
    path('enquiries', EnquiryListCreate.as_view(), name='enquiries'),
    path('transaction-details/', TransactionDetailsListView.as_view(), name='transaction-details-list'),

    



]