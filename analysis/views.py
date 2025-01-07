from django.shortcuts import render
from account.models import *
from blogsapi.models import *
from adsapi.models import *
from profileapi.models import *
from pagesapi.models import *
import pandas as pd
from django.http import HttpResponse
import csv
# Create your views here.
# data= pd.read_csv('users.csv')
# data1= pd.read_csv('blogs.csv')
# data2= pd.read_csv('contacts.csv')
# data3= pd.read_csv('products.csv')
# data4= pd.read_csv('profile.csv')



# df = pd.DataFrame(data)
# df.drop_duplicates(inplace = True)
# print(df.to_string())
def users(request):
    users = User.objects.all()
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=users.csv'
    writer = csv.writer(response)
    writer.writerow(['email', 'name', 'tc', 'is_active', 'is_admin','created_at','phoneNumber','updated_at','auth_provider'])
    user = users.values_list('email', 'name', 'tc', 'is_active', 'is_admin','created_at','phoneNumber','updated_at','auth_provider')
    for std in user:
        writer.writerow(std)
    return response

def blogs(request):
    blogs = Blogs.objects.all()
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=blogs.csv'
    writer = csv.writer(response)
    writer.writerow(['user', 'category', 'title', 'description','state','city','author','published_time','subtitle'])
    blog = blogs.values_list('user', 'category', 'title', 'description','state','city','author','published_time','subtitle')
    for std in blog:
        writer.writerow(std)
    return response

def profile(request):
    profiles = Profile.objects.all()
    response = HttpResponse('')
    response['Content-Disposition'] = 'attachment; filename=profiles.csv'
    writer = csv.writer(response)
    writer.writerow(['user','name','email','PhoneNumber','address','state','city','zipcode'])
    profile = profiles.values_list('user','name','email','PhoneNumber','address','state','city','zipcode')
    for std in profile:
        writer.writerow(std)
    return response

def ads(request):
    products = Product.objects.all()
    response = HttpResponse('')
    response['Content-Disposition'] = 'attachment; filename=products.csv'
    writer = csv.writer(response)
    writer.writerow(['user','title','price','tags','brand','condition','state','date_created'])
    product = products.values_list('user','title','price','tags','brand','condition','state','date_created')
    for std in product:
        writer.writerow(std)
    return response

def pages(request):
    contacts = Contact.objects.all()
    response = HttpResponse('')
    response['Content-Disposition'] = 'attachment; filename=contacts.csv'
    writer = csv.writer(response)
    writer.writerow(['Name','Email','PhoneNumber','Message'])
    contact = contacts.values_list('Name','Email','PhoneNumber','Message')
    for std in contact:
        writer.writerow(std)
    return response
import ast
# import json
def telemtrydaa(request):
    telemtrydaas = TelemetryDaa.objects.all()
    response = HttpResponse('')
    response['Content-Disposition'] = 'attachment; filename=telemtrydaa.csv'
    writer = csv.writer(response)
    writer.writerow(['id','home','contactForm','about','faq','DashAds','Refundpolicy','Listingpolicy','Copyrightpolicy','Terms','Privacypolicy','HomeRealEsate','ShowBlog','UpdateBlog',"AddBlog","BlogDetails","ForgotPassword","ShowBlog","AddProduct","ProductDetails","UpdateProduct","ShowProduct","Pricing","ActivePlans","Dashboard","Profile","Wishlist","Signup","Login","CheckOTP","Logout","YouTubeChannel","EdistAds","chatWithAdmin"])
    telemtrydaa = telemtrydaas.values_list("id","home","contactForm","about","faq","DashAds","Refundpolicy","Listingpolicy","Copyrightpolicy","Terms","Privacypolicy","HomeRealEsate","ShowBlog","UpdateBlog","AddBlog","BlogDetails","ForgotPassword","ShowBlog","AddProduct","ProductDetails","UpdateProduct","ShowProduct","Pricing","ActivePlans","Dashboard","Profile","Wishlist","Signup","Login","CheckOTP","Logout","YouTubeChannel","EdistAds","chatWithAdmin")
    for std in telemtrydaa:
        writer.writerow(std)
    return response
# def telemtrydaa(request):
#     telemtrydaa = TelemetryDaa.objects.all()
#     a=[]
#     for x in telemtrydaa:
#         value= ast.literal_eval(x.data)
#         # print(type(value))
#         a.append(value)
#     finalDataKeys=["id","home","contactForm","about","faq","DashAds","Refundpolicy","Listingpolicy","Copyrightpolicy","Terms","Privacypolicy","HomeRealEsate","ShowBlog","UpdateBlog","AddBlog","BlogDetails","ForgotPassword","ShowBlog","AddProduct","ProductDetails","UpdateProduct","ShowProduct","Pricing","ActivePlans","Dashboard","Profile","Wishlist","Signup","Login","CheckOTP","Logout","YouTubeChannel","EdistAds","chatWithAdmin"]
#     finalObject={}
#     for x in finalDataKeys:
#         tempList=[] 
#         for y in a:
#             tempList.append(y[x])
#         finalObject[x]=tempList
#     # print(finalObject)
#     df=pd.DataFrame(finalObject)
    
#     # print(df)
#     # dataframe=pd.DataFrame(df,columns=["id","home","contactForm","about","faq","DashAds","Refundpolicy","Listingpolicy","Copyrightpolicy","Terms","Privacypolicy","HomeRealEsate","ShowBlog","UpdateBlog","AddBlog","BlogDetails","ForgotPassword","ShowBlog","AddProduct","ProductDetails","UpdateProduct","ShowProduct","Pricing","ActivePlans","Dashboard","Profile","Wishlist","Signup","Login","CheckOTP","Logout","YouTubeChannel","EdistAds","chatWithAdmin"])
    

    

# # convert pandas dataframe to csv without index
#     response=df.to_csv("telemtrydaa.csv",index=True)
#     return HttpResponse (response)