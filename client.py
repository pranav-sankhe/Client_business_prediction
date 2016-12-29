import urllib
import urllib2
import pandas as pd
import json 
from sklearn.externals import joblib
from sklearn import svm
import schedule
import time
import MySQLdb

prev_length = 0 	

def account_id(account_dict,deal_dict):
	account_dict = account_dict['response']['result']['Accounts']['row']
 	deal_dict = deal_dict['response']['result']['Accounts']['row']

 	l = []

 	for i in range(len(deal_dict)):
		for j in  range(len(deal_dict[i]['FL'])):
			if deal_dict[i]['FL'][j]['val'] == 'Stage':
				if deal_dict[i]['FL'][j]['content'] == 'Closed (Won)' :
					for l in range(len(account_dict[i]['FL'])):
						if account_dict[i]['FL'][l]['val'] == 'ACCOUNTID':
							l.append(account_dict[i]['FL'][l]['content'])

	return l
def pred_account_id(account_dict,deal_dict):
	account_dict = account_dict['response']['result']['Accounts']['row']
 	deal_dict = deal_dict['response']['result']['Accounts']['row']

 	l = []

 	for i in range(len(deal_dict)):
		for j in  range(len(deal_dict[i]['FL'])):
			if deal_dict[i]['FL'][j]['val'] == 'Stage':
				if deal_dict[i]['FL'][j]['content'] != 'Closed (Won)' :
					for l in range(len(account_dict[i]['FL'])):
						if account_dict[i]['FL'][l]['val'] == 'ACCOUNTID':
							l.append(account_dict[i]['FL'][l]['content'])

	return l

def ann_revenue(account_dict,deal_dict):
	account_dict = account_dict['response']['result']['Accounts']['row']
	l = []

 	for i in range(len(deal_dict)):
		for j in  range(len(deal_dict[i]['FL'])):
			if deal_dict[i]['FL'][j]['val'] == 'Stage':
				if deal_dict[i]['FL'][j]['content'] == 'Closed (Won)' :
					for l in range(len(account_dict[i]['FL'])):
						if account_dict[i]['FL'][l]['val'] == 'Annual Revenue':
							l.append(account_dict[i]['FL'][l]['content'])

	return l 			
def pred_revenue(account_dict,deal_dict):
	account_dict = account_dict['response']['result']['Accounts']['row']
	l = []

 	for i in range(len(deal_dict)):
		for j in  range(len(deal_dict[i]['FL'])):
			if deal_dict[i]['FL'][j]['val'] == 'Stage':
				if deal_dict[i]['FL'][j]['content'] != 'Closed (Won)' :
					for l in range(len(account_dict[i]['FL'])):
						if account_dict[i]['FL'][l]['val'] == 'Annual Revenue':
							l.append(account_dict[i]['FL'][l]['content'])

	return l 				

def location(account_dict,deal_dict):
	account_dict = account_dict['response']['result']['Accounts']['row']
	l = []

 	for i in range(len(deal_dict)):
		for j in  range(len(deal_dict[i]['FL'])):
			if deal_dict[i]['FL'][j]['val'] == 'Stage':
				if deal_dict[i]['FL'][j]['content'] == 'Closed (Won)' :
					for l in range(len(account_dict[i]['FL'])):
						if account_dict[i]['FL'][l]['val'] == 'Annual Revenue':
							code = account_dict[i]['FL'][l]['content']
							pincode = int(code[0] + code[1])
							l.append(pincode)
	return l 
def pred_location(account_dict,deal_dict):
	account_dict = account_dict['response']['result']['Accounts']['row']
	l = []

 	for i in range(len(deal_dict)):
		for j in  range(len(deal_dict[i]['FL'])):
			if deal_dict[i]['FL'][j]['val'] == 'Stage':
				if deal_dict[i]['FL'][j]['content'] != 'Closed (Won)' :
					for l in range(len(account_dict[i]['FL'])):
						if account_dict[i]['FL'][l]['val'] == 'Annual Revenue':
							code = account_dict[i]['FL'][l]['content']
							pincode = int(code[0] + code[1])
							l.append(pincode)
	return l 

def amount(deal_dict):
	deal_dict = deal_dict['response']['result']['Deals']['row']
	l = []
	for i in range(len(deal_dict)):
		for j in range(len(deal_dict[i]['FL'])):
			if deal_dict[i]['FL'][j]['val'] == 'Amount':
				l.append(deal_dict[i]['FL'][j]['content'])
	return l 				
def turnaround_Time(deal_dict):
	deal_dict = deal_dict['response']['result']['Deals']['row']
	l = []
	for i in range(len(deal_dict)):
		for j in range(len(deal_dict[i]['FL'])):
			if deal_dict[i]['FL'][j]['val'] == 'Sales Cycle Duration':
				l.append(deal_dict[i]['FL'][j]['content'])
	return l 			
def deal_status(deal_dict):
	deal_dict = deal_dict['response']['result']['Deals']['row']
	
	
	for j in range(len(deal_dict[0]['FL'])):
		if deal_dict[0]['FL'][j]['val'] == 'Stage':
			l = deal_dict[0]['FL'][j]['content'] 
	return l 				

def request_account_data(token):
	module_name = 'Accounts'
	authtoken = token
	params = {'authtoken':authtoken,'scope':'crmapi'}      
	final_URL = "https://crm.zoho.com/crm/private/json/"+module_name+"/getRecords"
	data = urllib.urlencode(params)
	request = urllib2.Request(final_URL,data)
	response = urllib2.urlopen(request)
	json_response = response.read()
	d = json.loads(json_response)
	return d
def request_deals_data(token):
	module_name = 'Deals'
	authtoken = token
	params = {'authtoken':authtoken,'scope':'crmapi'}
	final_URL = "https://crm.zoho.com/crm/private/json/"+module_name+"/getRecords"
	data = urllib.urlencode(params)
	request = urllib2.Request(final_URL,data)
	response = urllib2.urlopen(request)
	json_response = response.read()
	d = json.loads(json_response)
	return d

	#def add_account(token):
def request_leads_data(token):
	module_name = 'Leads'
	authtoken = token
	params = {'authtoken':authtoken,'scope':'crmapi'}
	final_URL = "https://crm.zoho.com/crm/private/json/"+module_name+"/getRecords"
	data = urllib.urlencode(params)
	request = urllib2.Request(final_URL,data)
	response = urllib2.urlopen(request)
	json_response = response.read()
	d = json.loads(json_response)
	return d

def predict(Input):

	token  = Input
	
	#----------------------------------
	#    Get data via zoho api 	
	account_d = request_account_data(token)
	deal_d = request_deals_data(token)
	global prev_length
	length = len(deal_d)
	
	if length > prev_length:

		val = length - prev_length
		#------------------------------------------
		#            Training Data

		acc_ids = account_id(account_d,deal_d)
		cust_revenue = ann_revenue(account_d,deal_d)    
		locate = location(account_d,deal_d)

		#------------------------------------------
		#			Values to be predicted
		b_amount = amount(deal_d)
		tTime = turnaround_Time(deal_d)

		fitX = pd.DataFrame(
	    {'revenue': cust_revenue,
	     'location': locate
	    })


		
		clf_time = svm.SVC()
		clf.fit(fitX, tTime)
		
		clf_amount = svm.SVC()
		clf.fit(fitX, b_amount)
		
		

		revenue = []
		pLocation = [] 
		pAccount =[]
		for i in range(length - prev_length):
			revenue.append(pred_revenue(account_d,deal_d))
			cLocation.append(pred_location(account_d,deal_d))
			pAccount.append(pred_location(account_d,deal_d))
		
	
		pred_data = pd.DataFrame(
			{ 'revenue' : revenue,
			  'location' : cLocation
			}
			)


		
		pred_amount = clf_amount.predict(pred_data) 
		pred_time =  clf_time.predict(pred_data) 
		
		dataframe = pd.DataFrame(

			{ 'accounID' : pAccount,
			 'buisness amount' : pred_amount,
			  'Turnaround time' : pred_time 	
			}
			)

		prev_length = length
		
		if val > 0 :
			return dataframe 	
		else: 
			return "no new entries"


def getAllTokens():
	# query DB for all tokens
	db = MySQLdb.connect("http://localhost:8080/","user","password","TESTDB" )
	cursor = db.cursor()	

	query = "select email, token from auth_user"
	
	cursor.execute(query)
	results = cursor.fetchall()

	for result in results:
		# execute predict with the result token
		predictions = predict(result.token)
		# send mail 
		#http://arrowbot.net/rpc/channel/1c476c99-604b-4dce-9553-552e5a94e4aa/invoke?rcpt_to=ujj.shukla@gmail.com&subject=hello&body=hello
		email = result.email
		request = urllib2.Request("http://arrowbot.net/rpc/channel/1c476c99-604b-4dce-9553-552e5a94e4aa/invoke?rcpt_to=" + str(email) + "&subject="+ str(predictions))		

def main(token):
	
	# Open database connection
	# db = MySQLdb.connect("http://localhost:8080/","user","password","TESTDB" )
	# cursor = db.cursor()	

	# query = "select (email),(token) from auth_user"
	
	# cursor.execute(query)
	# results = cursor.fetchall()


	schedule.every(10).minutes.do(getAllTokens)

	while True:
		schedule.run_pending()
		time.sleep(1)


