import json
import environ
import razorpay
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from account.models import User
env = environ.Env()
from rest_framework import generics
environ.Env.read_env()
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
import http.client
import urllib.request
import urllib.parse
import json
import hmac
import hashlib
import base64
from adsapi.models import *

accesskey="a2b08960-86b3-11ed-a1b9-ffe33bc79fc2"
secretkey="6f7d9ce55c3225408200999df006c21941a20e8f"
environment="test"




remote_script="https://payments.open.money/layer"
sample_data = dict()
sample_data["amount"] = "12.00"
sample_data["currency"] = "INR"
sample_data["name"] = "John Doe"
sample_data["email_id"]="john.doe@dummydomain.com"
sample_data["contact_number"]= "9831111111"
sample_data["mtx"]= ""
sample_data["empty"]=""



BASE_URL_SANDBOX = "sandbox-icp-api.bankopen.co";
BASE_URL_UAT = "icp-api.bankopen.co";					   



class EnquiryListCreate(generics.ListCreateAPIView):
    queryset = Enquiry.objects.all()
    serializer_class = EnquirySerializer



@csrf_exempt
def index(request):
	global accesskey,secretkey,environment,remote_script,sample_data
	error=""
	layer_payment_token_data=dict()
	payment_token_data = dict()
	token_id=""
	hash = ""
	layer_params=""
	sample_data["mtx"] = random.randint(1,200)
	
	
	layer_payment_token_data = create_payment_token(sample_data,accesskey,secretkey,environment)
	
	if layer_payment_token_data:
		for k in layer_payment_token_data.keys():
			if k == "error":
				error = layer_payment_token_data[k]
		
	if len(error) == 0 and len(layer_payment_token_data["id"]) < 1:
		error="E55 Payment error. Token data empty."
			
	if len(error) == 0 and len(layer_payment_token_data["id"]) > 0:
		payment_token_data = get_payment_token(layer_payment_token_data["id"],accesskey,secretkey,environment)
	
	if payment_token_data:		
		for k in payment_token_data.keys():
			if k == "error":
				error = payment_token_data[k]
				
	if len(error) == 0 and len(payment_token_data["id"]) < 1:
		error="Payment error. Layer token ID cannot be empty."
		
	if len(error) == 0 and len(payment_token_data["id"]) > 0 and payment_token_data["status"]=="paid": 
		error="Layer: this order has already been paid."
		
	if len(error) == 0 and str(payment_token_data["amount"]) != str(sample_data["amount"]): 
		error="Layer: an amount mismatch occurred."
		
	if error == "":
		gen = dict()
		gen["amount"]=payment_token_data["amount"]
		gen["id"]=payment_token_data["id"]
		gen["mtx"]=sample_data["mtx"]
		hash=create_hash(gen,accesskey,secretkey)		
		layer_params = "{payment_token_id:"+payment_token_data["id"]+",accesskey:"+accesskey+"}"
		token_id=payment_token_data["id"]
		
	
	return render(request,
	'layerpayment/checkout.html',
	{'txnid':str(sample_data["mtx"]),
	'fullname':sample_data["name"],
	'email':sample_data["email_id"],
	'mobile':sample_data["contact_number"],
	'amount':str(sample_data["amount"]),
	'currency':sample_data["currency"],
	'remote_script':remote_script,
	'token_id':token_id,
	'hash':hash,
	'accesskey':accesskey,
	'layer_params':layer_params,
	'error':error})


from rest_framework.views import APIView
import json

class callback_class(APIView):
	def post( self,request , format=None):
		global accesskey,secretkey,environment
		error=""
		status=""
		payment_data=dict()
	
		# response = request.POST
		reponse1=request.data
		print("----------------reponse",reponse1)
		if len(response["layer_payment_id"]) == 0:
			error = "Invalid payment id"
		if len(error)==0:
			vhash=dict()
			vhash["amount"] =response["layer_order_amount"]
			vhash["id"]=response["layer_pay_token_id"]
			vhash["mtx"]=response["tranid"]
			if not verify_hash(vhash,response["hash"],accesskey,secretkey):
				error="Invalid payment response...Hash mismatch"
		if len(error) == 0:
			payment_data = get_payment_details(response["layer_payment_id"],accesskey,secretkey,environment)
	
		if payment_data:
			for k in payment_data.keys():
				if k == "error":
					error = payment_data[k]
		if len(error) == 0 and payment_data["payment_token"]["id"] != response["layer_pay_token_id"]:
			error = "Layer: received layer_pay_token_id and collected layer_pay_token_id doesnt match"
		if len(error) == 0 and payment_data["amount"] != response["layer_order_amount"]:
			error = "Layer: received amount and collected amount doesnt match"
		if len(error) == 0 and payment_data["payment_token"]["status"] != "paid":
			status = "Transaction failed..."+payment_data["payment_error_description"]
		elif len(error) == 0:
			status = "Transaction Successful"
		data={'errorstring':error,'status':status}
		print(data)
		return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt	
def callback(request):
	global accesskey,secretkey,environment
	error=""
	status=""
	payment_data=dict()
	
	response = request.POST
	print("Received data:", response)

	print("----------------reponse",response,response["layer_pay_token_id"])
 	
	if len(response["layer_payment_id"]) == 0:
		error = "Invalid payment id"
	if len(error)==0:
		vhash=dict()
		vhash["amount"] =response["layer_order_amount"]
		vhash["id"]=response["layer_pay_token_id"]
		vhash["mtx"]=response["tranid"]
		if not verify_hash(vhash,response["hash"],accesskey,secretkey):
			error="Invalid payment response...Hash mismatch"
	if len(error) == 0:
		payment_data = get_payment_details(response["layer_payment_id"],accesskey,secretkey,environment)
	
	if payment_data:
		for k in payment_data.keys():
			if k == "error":
				error = payment_data[k]
	if len(error) == 0 and payment_data["payment_token"]["id"] != response["layer_pay_token_id"]:
		error = "Layer: received layer_pay_token_id and collected layer_pay_token_id doesnt match"
	if len(error) == 0 and payment_data["amount"] != response["layer_order_amount"]:
		error = "Layer: received amount and collected amount doesnt match"
	if len(error) == 0 and payment_data["payment_token"]["status"] != "paid":
		status = "Transaction failed..."+str(payment_data["payment_error_description"] if payment_data["payment_error_description"] else "")
	elif len(error) == 0:
		status = "Transaction Successful"
	data={'errorstring':error,'status':status}
	finalData={}
	finalData["errorstring"]=data["errorstring"]
	finalData["status"]=data["status"]
	s=TransactionDetails.objects.get(payment_token_id=response["layer_pay_token_id"])
	s.refresh_from_db()
	s.payment_id=response["layer_payment_id"]
	if status=="Transaction Successful" and s.paymentStatus != "Success":
		s.paymentStatus="Success"
		finalData["status"]="Success"
		finalData["payment_id"]=response["layer_payment_id"]
		finalData["plan"]=s.plan
		finalData["email"]=s.email
		finalData["transactionId"]=s.tranid
		finalData["amount"]=s.order_payment_amount   
		finalData["phoneNumber"]=s.phoneNumber
		finalData["name"]=s.userID.name
		json1_file = open('C:/Users/91910/Downloads/compressed_filename/hola9DjangoLatest/paymentapi/json/pricingPlan.json','r+', encoding="utf-8")
		planJsonOBJ=json.load(json1_file)
		planJsonOBJ1 = open('C:/Users/Downloads/compressed_filename/hola9DjangoLatest/paymentapi/json/businessPlan.json','r+', encoding="utf-8")
		businessProfile=json.load(planJsonOBJ1)
		user=s.userID
		print("json data printing here",json1_file)
		
		OrderID=response["layer_payment_id"]

		if s.plan == "Premium":
			category = s.plan
			validity = s.monthsVale
			city = businessProfile["Premium"]["city"]
			visiblity = businessProfile["Premium"]["visiblity"]
			teleSupport = businessProfile["Premium"]["teleSupport"]
			chatSupport = businessProfile["Premium"]["chatSupport"]
			dedicatedRm = businessProfile["Premium"]["dedicatedRm"] 
			hol9Website = businessProfile["Premium"]["hola9Website"]

			x = BusinessPricing.objects.create(
				user=user, category=category, validity=validity, visiblity=visiblity,
				NoAds=s.adsValue, OrderID=OrderID, city=s.City,
				teleSupport=teleSupport, chatSupport=chatSupport,
				dedicatedRm=dedicatedRm, hol9Website=hol9Website
			)
			
			finalData["category"] = category
			finalData["validity"] = validity
			finalData["city"] = city
			finalData["visiblity"] = visiblity
			finalData["teleSupport"] = teleSupport
			finalData["chatSupport"] = chatSupport
			finalData["dedicatedRm"] = dedicatedRm
			finalData["hol9Website"] = hol9Website
   
		elif s.plan == "Featured":
			# category = businessProfile["Featured"]["category"]
			category = s.plan
			# validity = businessProfile["Featured"]["selectmonths"]
			validity = s.monthsVale
			city = businessProfile["Featured"]["city"]
			visiblity = businessProfile["Featured"]["visiblity"]
			teleSupport = businessProfile["Featured"]["teleSupport"]
			chatSupport = businessProfile["Featured"]["chatSupport"]
			dedicatedRm = businessProfile["Featured"]["dedicatedRm"]
			hol9Website = businessProfile["Featured"]["hola9Website"]

			x = BusinessPricing.objects.create(
				user=user, category=category, validity=validity, city=s.City,
				visiblity=visiblity, NoAds=s.adsValue, OrderID=OrderID,
				teleSupport=teleSupport, chatSupport=chatSupport,
				dedicatedRm=dedicatedRm, hol9Website=hol9Website
			)
			
			finalData["category"] = category
			finalData["validity"] = validity
			finalData["city"] = city
			finalData["visiblity"] = visiblity
			finalData["teleSupport"] = teleSupport
			finalData["chatSupport"] = chatSupport
			finalData["dedicatedRm"] = dedicatedRm
			finalData["hol9Website"] = hol9Website
		elif s.plan=="VerifiedCustomer":
			x=VerifiedCustomerMain.objects.create(userid=user,plan_type=s.plan,price=234,validity=30,OrderID=OrderID)
		else:
			planData=planJsonOBJ[s.plan]
			category =planData["category"]
			days =planData["days"]
			regulars =planData["regulars"] 
			# topAds =planData["topAds"]
			# featured=planData["featured"]
			teleSupport=planData["teleSupport"]
			response=planData["response"]
			chatSupport=planData["chatSupport"]
			dedicatedRm=planData["dedicatedRm"]
			hol9Website=planData["hola9Website"]
			validity=planData["validity"] 
			x=Pricing.objects.create(user=user,category=category,days=days,regulars=regulars,teleSupport=teleSupport,response=response,chatSupport=chatSupport,dedicatedRm=dedicatedRm,hol9Website=hol9Website,OrderID=OrderID,validity=validity)
			finalData["days"]=days
			finalData["regulars"]=regulars
			# finalData["topAds"]=topAds
			# finalData["featured"]=featured
			finalData["teleSupport"]=teleSupport
			finalData["response"]=response
			finalData["chatSupport"]=chatSupport
			finalData["dedicatedRm"]=dedicatedRm
			finalData["hol9Website"]=hol9Website
		x.save()
		s.save()
	else:
		s.refresh_from_db()
		s.paymentStatus="Failed"
		s.save()

	print(data,payment_data)
	return HttpResponse(json.dumps(finalData), content_type='application/json')
	


def create_payment_token(data,accesskey,secretkey,environment):

	response=dict()
	
	try:
		emptykeys=[]
		for k in data.keys():
			if len(str(data[k]))<1:
				emptykeys.append(k)
		for i in emptykeys:
			del data[i]
		response = http_post(data,"payment_token",accesskey,secretkey,environment)
	except Exception as ex:			
		response["error"]=ex
	return response



from rest_framework.views import APIView
import json
class create_payment_token_Class(APIView):
	def post( self,request , format=None):
		global accesskey,secretkey,environment,remote_script,sample_data
		data = dict()
		error=""
		layer_payment_token_data=dict()
		payment_token_data = dict()
		token_id=""
		hash = "" 
		layer_params=""
		adsValue=request.data.get("adsValue")
		monthsVale=request.data.get("monthsVale")
		planJsonOBJ = open('C:/Users/91910/Downloads/compressed_filename/hola9DjangoLatest/paymentapi/json/businessPlan.json','r+', encoding="utf-8")
		businessProfile=json.load(planJsonOBJ)
		print("businessProfilePlanVALUE",businessProfile)
		name=request.data.get("IdValue")
		planValue=request.data.get("planValue")
		adsCategory=request.data.get("adsCategory")
		if planValue=="Silver":
			data["amount"] = str(99+(99*18/100))
		elif planValue=="VerifiedCustomer":
			data["amount"] =str(199+(299*18/100))
		elif planValue=="Gold":
			data["amount"] =str(299+(299*18/100))
		elif planValue=="Platinum":
			data["amount"] = str(int(799+(799*18/100)))+".00"
		elif planValue=="Premium":
			category_prices = businessProfile['Premium']['adscategory'][adsCategory]
			priceData=int(request.data.get("PriceValue"))
			print("pricing data ",priceData,type(priceData))
			data["amount"]=str(int(priceData+(priceData*18/100)))+".00"  # need to put dynamic value here also that one 
			print("data[amount]...........",data["amount"])
		elif planValue=="Featured":
			category_prices = businessProfile['Featured']['adscategory'][adsCategory]
			data["amount"]=str(int(category_prices+(category_prices*18/100)))+".00"   # need to put dynamic value here also that one 
		else:
			data["amount"] = ""
		print(name,planValue,data["amount"])
		userData=User.objects.get(pk=name)
		data["name"] =userData.name
		data["email_id"]=userData.email
		data["contact_number"]=request.data.get("Phone")
		data["currency"] = "INR"
		data["mtx"]= random.randint(1,2000000)
		data["empty"]=""
		
		response=dict()
		try:
			emptykeys=[]
			for k in data.keys():
				if len(str(data[k]))<1:
					emptykeys.append(k)
			for i in emptykeys:
				del data[i]
			response = http_post(data,"payment_token",accesskey,secretkey,environment)
			print("@@@@@@@reponse",response)
		except Exception as ex:			
			response["error"]=ex
		print(response)
		layer_payment_token_data=response
		if layer_payment_token_data:
			for k in layer_payment_token_data.keys():
				if k == "error":
					error = layer_payment_token_data[k]
		if len(error) == 0 and len(layer_payment_token_data["id"]) < 1:
			error="E55 Payment error. Token data empty."
			
		if len(error) == 0 and len(layer_payment_token_data["id"]) > 0:
			payment_token_data = get_payment_token(layer_payment_token_data["id"],accesskey,secretkey,environment)
		print("payment_token_data",payment_token_data)
		if payment_token_data:		
			for k in payment_token_data.keys():
				if k == "error":
					error = payment_token_data[k]



		if len(error) == 0 and len(payment_token_data["id"]) < 1:
			error="Payment error. Layer token ID cannot be empty."
		
		if len(error) == 0 and len(payment_token_data["id"]) > 0 and payment_token_data["status"]=="paid": 
			error="Layer: this order has already been paid."
		
		if len(error) == 0 and str(payment_token_data["amount"]) != str(data["amount"]): 
			error="Layer: an amount mismatch occurred."
		if error == "":
			gen = dict()
			gen["amount"]=payment_token_data["amount"]
			gen["id"]=payment_token_data["id"]
			gen["mtx"]=data["mtx"]
			hash=create_hash(gen,accesskey,secretkey)		
			layer_params = "{payment_token_id:"+payment_token_data["id"]+",accesskey:"+accesskey+"}"
			token_id=payment_token_data["id"]
        
		if len(error) == 0:
			if payment_token_data["status"]=="paid":
				assign_payment_status = "Success"
			else:
				assign_payment_status = "Pending"
		else:
			if payment_token_data["status"]=="paid":
				assign_payment_status = "Success"
			else:
				assign_payment_status = f"Failed...{error}"

		if not TransactionDetails.objects.filter(payment_token_id=token_id).exists():
			s=TransactionDetails.objects.create(payment_token_id=token_id,payment_id="",userID_id=name,plan=planValue,paymentStatus=assign_payment_status,email=data["email_id"],tranid=data["mtx"],order_payment_amount=data["amount"],phoneNumber=data["contact_number"],adsValue=adsValue,monthsVale=monthsVale,City=request.data.get("city"))
		else:
			s=TransactionDetails.objects.get(payment_token_id=token_id)
			s.paymentStatus = assign_payment_status
			s.save()
		obj={'txnid':str(data["mtx"]),
		'fullname':data["name"],
		'email':data["email_id"],
		'mobile':data["contact_number"],
		'amount':str(data["amount"]),
		'currency':data["currency"],
		'remote_script':remote_script,
		'token_id':token_id,
		'hash':hash,
		'accesskey':accesskey,
		'layer_params':layer_params,
		'error':error}
		print("last output",obj)
		return HttpResponse(json.dumps(obj), content_type='application/json')



def get_payment_token(payment_token_id,accesskey,secretkey,environment):
	response=dict()
	try:
		if len(payment_token_id)==0 or payment_token_id.isspace():
			response["error"]="payment_token_id cannot be empty"				
		else:
			response = http_get("payment_token/" + payment_token_id,accesskey,secretkey,environment)
	except Exception as ex:
		response["error"] = ex
	
	return response
	

def get_payment_details(payment_id,accesskey,secretkey,environment):
	response=dict()
	try:
		if len(payment_id)==0 or payment_id.isspace():			
			response["error"]="pyment_id cannot be empty"	
		else:
			response=http_get("payment/"+payment_id,accesskey,secretkey,environment)
	except Exception as ex:
		response["error"] = ex
	
	return response
	

def http_post(data,route,accesskey,secretkey,environment):
	response = ""
	url = BASE_URL_SANDBOX 
	if environment == "live":
		url = BASE_URL_UAT 
	
	resource = "/api/"+route
	
	try:
		conn = http.client.HTTPSConnection(url,timeout=10)
		headers = {'Content-type': 'application/json',"Authorization":"Bearer "+accesskey+":"+secretkey}
		jdata = json.dumps(data)
		conn.request('POST', resource, jdata, headers)
		resp = conn.getresponse()		
		rdata = resp.read().decode('utf-8')
		conn.close()
		response = json.loads(rdata)		
	except Exception as ex:
		print(ex)
	
	return response
	
def http_get(route,accesskey,secretkey,environment):
	response = ""
	url = BASE_URL_SANDBOX 
	if environment == "live":
		url = BASE_URL_UAT 
	resource = "/api/"+route
	
	try:
		conn = http.client.HTTPSConnection(url,timeout=10)
		headers = {'Content-type': 'application/json',"Authorization":"Bearer "+accesskey+":"+secretkey}
		conn.request("GET", resource,"",headers)
		resp = conn.getresponse()
		rdata = resp.read().decode('utf-8')
		conn.close()
		response = json.loads(rdata)
	except Exception as ex:
		print(ex)
	
	return response
	
	
def create_hash(data,accesskey,secretkey):
	hash=""
	try:
		pipeSeperatedString=accesskey+"|"+str(data["amount"])+"|"+data["id"]+"|"+str(data["mtx"])
		signature = hmac.new(
			bytes(secretkey , 'latin-1'),  
			msg = bytes(pipeSeperatedString , 'latin-1'), 
			digestmod = hashlib.sha256).hexdigest().upper()
		
		base64_bytes = base64.b64encode(signature.encode('ascii'))
		hash = base64_bytes.decode('ascii')
		 
	except Exception as ex:
		hash = ex
		
	return hash
	

def verify_hash(data,rec_hash,accesskey,secretkey):
	gen_hash = create_hash(data,accesskey,secretkey)
	if gen_hash == rec_hash:
		return True
	else:
		return False

from django.core import serializers
from django.http import HttpResponse

class userTransData(APIView):
    def post(self, request, format=None):
        # Get the userID from the request data
        userID = request.data.get('userID')

        # Get the limit from the request data (default to None if not provided)
        limit_str = request.data.get('limit', None)
        limit = int(limit_str) if limit_str is not None else None

        # Filter TransactionDetails by userID and apply the limit
        queryset = TransactionDetails.objects.filter(userID_id=userID)[:limit]

        # Serialize the queryset to JSON
        data = serializers.serialize('json', queryset)

        # Return the JSON response
        return HttpResponse(data, content_type='application/json')

class TransactionDetailsListView(APIView):
    def get(self, request, format=None):
        user_id = request.query_params.get('user_id')

        if user_id is not None:
            transaction_details = TransactionDetails.objects.filter(userID=user_id)
        else:
            transaction_details = TransactionDetails.objects.all()

        serializer = TransactionDetailsSerializer(transaction_details, many=True)
        return Response(serializer.data)

