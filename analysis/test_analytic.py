# import csv
# import pandas as pd
# import pandas as pd

# df = pd.read_csv('telemtrydaa.csv')
# df['home'] = df['home'].str.split(',')
# df['contactForm'] = df['contactForm'].str.split(',')
# df['about'] = df['about'].str.split(',')
# df['AddBlog'] = df['AddBlog'].str.split(',')
# df['BlogDetails'] = df['BlogDetails'].str.split(',')
# df['AddProduct'] = df['AddProduct'].str.split(',')
# df['ProductDetails'] = df['ProductDetails'].str.split(',')
# df['ShowProduct'] = df['ShowProduct'].str.split(',')
# df['Profile'] = df['Profile'].str.split(',')
# df['Signup'] = df['Signup'].str.split(',')
# df['Login'] = df['Login'].str.split(',')
# df['chatWithAdmin'] = df['chatWithAdmin'].str.split(',')



# # convert list of pd.Series then stack it
# dd = (df.set_index(['id','faq','DashAds','Refundpolicy','Listingpolicy','Copyrightpolicy','Terms','Privacypolicy','HomeRealEsate','ShowBlog','UpdateBlog','ForgotPassword','ShowBlog','UpdateProduct','Pricing','ActivePlans','Dashboard','Wishlist','CheckOTP','Logout','YouTubeChannel','EdistAds'])['home','contactForm','about','AddBlog','BlogDetails','AddProduct','ProductDetails','ShowProduct','Profile','Signup','Login','chatWithAdmin']
#  .apply(pd.Series)
#  .stack()
#  .reset_index())
	

# print(dd)

# dfs = pd.DataFrame(df)

# # Display Original DataFrames
# print("Created DataFrame:\n",dfs,"\n")

# # splitting cities column
# res = dfs.set_index(["id","home","contactForm","about","faq","DashAds","Refundpolicy","Listingpolicy","Copyrightpolicy","Terms","Privacypolicy","HomeRealEsate","ShowBlog","UpdateBlog","AddBlog","BlogDetails","ForgotPassword","ShowBlog","AddProduct","ProductDetails","UpdateProduct","ShowProduct","Pricing","ActivePlans","Dashboard","Profile","Wishlist","Signup","Login","CheckOTP","Logout","YouTubeChannel","EdistAds","chatWithAdmin"]).apply(lambda x: x.str.split(',').explode()).reset_index()

# # Display result
# print("Result:\n",res)
# df.drop_duplicates()
# df.dropna(subset=['home'], inplace = True)
# print(df)
# from hola9BackProd.account.models import *
# elemtrydaa = TelemetryDaa.objects.all()
# data= pd.read_csv('csv_data/users1.csv')
# data.drop_duplicates(inplace = None)
# # print(data.to_string())
# df=pd.read_csv('telemtrydaa.csv')

# import csv
# with open('telemtrydaa.csv','r') as csvfile:
#   reader = csv.reader(csvfile, delimiter=' ')
#   for row in reader:
#       str1 = ''.join(row) #Convert list into string
#       parts = str1.split(",")
#       print (parts[0:15])
# import csv

# inp_fname = 'telemtrydaa.csv'
# out_fname = 'transposed.csv'

# with open(inp_fname, 'r', newline='') as in_csvfile,open(out_fname, 'w', newline='') as out_csvfile:
#     reader = csv.reader(in_csvfile)
#     writer = csv.writer(out_csvfile)

#     for row in reader:
#         for v in row[0].rstrip(',').split(','):
#             writer.writerow([v] + row[1:])
# print('view: ', home.get('view'))

# print('search: ', home.get('search'))
# dfs=df.drop_duplicates(inplace = None)
# # dfs.home.str.split(pat=',',expand=True)
# print(dfs.to_string())
# Home=df.home.str.split(pat=',',expand=True)
# print(Home)
# Contact_Form=df.contactForm.str.split(pat=',',expand=True)
# print(Contact_Form)
# About=df.about.str.split(pat=',',expand=True)
# print(About)
# Add_Blog=df.AddBlog.str.split(pat=',',expand=True)
# print(Add_Blog)
# Blog_Details=df.BlogDetails.str.split(pat=',',expand=True)
# print(Blog_Details)
# Add_Product=df.AddProduct.str.split(pat=',',expand=True)
# print(Add_Product)
# Product_Details=df.ProductDetails.str.split(pat=',',expand=True)
# print(Product_Details)
# Show_Product=df.ShowProduct.str.split(pat=',',expand=True)
# print(Show_Product)
# Profiles=df.Profile.str.split(pat=',',expand=True)
# print(Profiles)
# Signups=df.Signup.str.split(pat=',',expand=True)
# print(Signups)
# Logins=df.Login.str.split(pat=',',expand=True)
# print(Logins)
# chatWith_Admin=df.chatWithAdmin.str.split(pat=',',expand=True)
# print(chatWith_Admin)
# Home=df.home.str.split(pat=',',expand=True)
# Home=df.home.str.split(pat=',',expand=True)
# df.assign(var1=df['var1'].str.split(',')).explode('var1')
# df[['view','search']]=df.home.str.split(',',expand=True)
# df[['view','contact']]=df.contactForm.str.split(',',expand=True)
# df[['view','openingForm']]=df.about.str.split(',',expand=True)
# df[['view','addBlogForm']]=df.AddBlog.str.split(',',expand=True)
# df[['view','newsLetter','blogForm']]=df.BlogDetails.str.split(',',expand=True)
# df[['view','newAds']]=df.AddProduct.str.split(',',expand=True)
# df[['view','contactDetailsAds','sendMessgaeAdsAdmin','comment']]=df.ProductDetails.str.split(',',expand=True)
# df[['view','searchBox']]=df.ShowProduct.str.split(',',expand=True)
# df[['view','editProfileUpdate']]=df.Profile.str.split(',',expand=True)
# df[['view','signUpForm']]=df.Signup.str.split(',',expand=True)
# df[['view','loginForm']]=df.Login.str.split(',',expand=True)
# df[['view','chatMessageAdmin']]=df.chatWithAdmin.str.split(',',expand=True)
# print(df)

# df1 = pd.DataFrame(df)
# df2=df1['home'].apply(pd.Series)
# df2 = df["id","home","contactForm","about","faq","DashAds","Refundpolicy","Listingpolicy","Copyrightpolicy","Terms","Privacypolicy","HomeRealEsate","ShowBlog","UpdateBlog","AddBlog","BlogDetails","ForgotPassword","ShowBlog","AddProduct","ProductDetails","UpdateProduct","ShowProduct","Pricing","ActivePlans","Dashboard","Profile","Wishlist","Signup","Login","CheckOTP","Logout","YouTubeChannel","EdistAds","chatWithAdmin"].apply(pd.Series)
# print(df2)
# df1=(df.set_index([ 'id', 'faq','DashAds','Refundpolicy','Listingpolicy','Copyrightpolicy','Terms','Privacypolicy','HomeRealEsate','ShowBlog','UpdateBlog','ForgotPassword','ShowBlog','UpdateProduct','Pricing','ActivePlans','Dashboard','Wishlist','CheckOTP','Logout','YouTubeChannel','EdistAds']).apply(lambda x: x.str.split(',').explode()).reset_index())
# df.columns = ['view', 'search','view','contact','view','openingForm','view','view','view','view','view','view','view','view','view','view','view','addBlogForm','view','newsLetter','blogForm','view','view','view','newAds','view','contactDetailsAds','sendMessgaeAdsAdmin','comment','view','view','searchBox','view','view','view','view','editProfileUpdate','view','view','signUpForm','view','loginForm','view','view','view','view','view','chatMessageAdmin','Id']
# print(df2.columns.tolist())
# print(df1)
# df_melt=pd.melt(df, id_vars=['id','home'],value_vars=['view','search'],var_name='home',value_name='home')

# df2=pd.melt(df, id_vars=["id","contactForm","about","faq","DashAds","Refundpolicy","Listingpolicy","Copyrightpolicy","Terms","Privacypolicy","HomeRealEsate","ShowBlog","UpdateBlog","AddBlog","BlogDetails","ForgotPassword","ShowBlog","AddProduct","ProductDetails","UpdateProduct","ShowProduct","Pricing","ActivePlans","Dashboard","Profile","Wishlist","Signup","Login","CheckOTP","Logout","YouTubeChannel","EdistAds","chatWithAdmin"], value_vars=['view']).drop('home',axis=1).sort_values('home')
# print(df2)
# df_pivot=df_melt.pivot(index=['id','home'], columns='view',values=['home'])
# print(df_pivot)# df=pd.DataFrame('telemtrydaa.csv')[0:5]
# results = []
# with open("telemtrydaa.csv") as csvfile:
#     reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) # change contents to floats
#     print(reader)
#     for row in reader: # each row is a list
#         results.append(row)

# print(dfs)

# print(df.to_string())


# # print (pd.merge(data,df))
# print(results)
# import pandas as pd
  
# # merging two csv files
# df = pd.concat(
#     map(pd.read_csv, ['csv_data/users.csv', 'csv_data/profile.csv']), ignore_index=True)
# print(df)

# Removing duplicate values
# import pandas as pd


# You don't need numpy or anything you can just do the unique-ify in one line, while importing the csv using pandas:

# import pandas as pd
# # df = pd.read_csv('csv_data/users1.csv', usecols=['text/csvemail', 'name']).drop_duplicates(keep='first')
# import matplotlib.pyplot as plt
# df = pd.read_csv('csv_data/telemtrydaa.csv')
# for x in df.index:
#   if df.loc[x, "name"] == 'imran':
#     df.drop(x, inplace = True)
# print(df.to_string())
# df.drop_duplicates(inplace = True)
# newdf = df.filter(items=["name", "tc"])==filter
# dfs = pd.DataFrame(df)

# myvar = pd.Series(df)

# print(myvar)
# print(df.corr())

import pandas as pd

with open('telemtrydaa1231.json', encoding='utf-8') as inputfile:
    df = pd.read_json(inputfile)

df.to_csv('telemtrydaa.csv', encoding='utf-8', index=False)