"""
Train Input Format:
{
	"file": "data.csv",
	"columnName" : {"amount": "amount(In Cr.)", "time": ["customer_creation_date","meeting_date" ]}
}

File Format:
Display Name	Job Title	City	State or Province	ZIP or Postal Code	Country or Region	Deal Closure
Chris Green		IT Manager	Redmond	Wa					98052				United States		5


Predict Input Format:
{
	"file": "test.csv"
}
"""
import pandas as pd
import numpy as np
from sklearn import datasets, linear_model, preprocessing
from collections import defaultdict
from sklearn.externals import joblib
from sklearn import svm
import re
from datetime import datetime



def pinCode(x):
	var = ''
	if type(x) == float:
		var = ''
	else:
		l = re.findall('\d+',x)
		for i in l:
			if len(i) == 6:
				var = i 
	return var		

def turnoverTime(x,start_date):
	for date in start_date:
		diff = abs(x - date).days
		return diff
	
def train(input):
	# input = {"file": "data.csv", "predict": "Time"}
	print input

	d = defaultdict(preprocessing.LabelEncoder)
	# def train(input):
	fileName = input['file']
	amountColumn = input["columnName"]["amount"]
	timeColumn = input['columnName']['time']
	#predictCol = input['predict'] 
	data = pd.read_csv(fileName)
	
	# if((input)['predict'] == 'amount(In Cr.)'):
		
	amountPredictColumn = amountColumn

	trainCols = [col for col in data.columns if col not in [amountPredictColumn] and col not in 'customer_id']
	X_amount = data[trainCols]
	fitX_amount = X_amount 

	fitX_amount['address_company'] = fitX_amount['address_company'].apply(pinCode)	
	
	del fitX_amount['meeting_date']
	del fitX_amount['customer_creation_date']

	
	fitX_amount = fitX_amount.apply(lambda x: x if (x.dtype == np.float64 or x.dtype == int or x.dtype ==  'datetime64') else d[x.name].fit_transform(x))
	fitX_amount = fitX_amount.astype(float)
	
	
	Y_amount = data[amountPredictColumn].astype(int)
	
	
	'''
	# Create linear regression object
	regr = linear_model.LinearRegression()

	# Train the model using the training sets
	regr.fit(fitX, Y)
	'''
	clf = svm.SVC()
	clf.fit(fitX_amount, Y_amount)

	joblib.dump(clf, 'amount.pkl')
	joblib.dump(d, 'amountd.pkl')
	
	



# if((input)['predict'] == 'turnoverTime'):
	
	trainCols = ['company_name', 'group_key_promoters','activity_company','address_company']
	X_time = data[trainCols]
	
	predictColumns = timeColumn
	
	X_time['address_company'] = X_time['address_company'].apply(pinCode)
	
	fitX_time = X_time.apply(lambda x: x if (x.dtype == np.float64 or x.dtype == int) else d[x.name].fit_transform(x))
	fitX_time = fitX_time.astype(float)
	
	fitY_time = data[predictColumns]
	fitY_time['customer_creation_date'] = fitY_time['customer_creation_date'].apply(lambda x: datetime.strptime((x.split(" ")[0]), "%Y/%m/%d"))
	fitY_time['meeting_date'] = fitY_time['meeting_date'].apply(lambda x: datetime.strptime((x), "%Y/%m/%d"))
	
	Y_time = fitY_time['meeting_date'] - fitY_time['customer_creation_date']
	
	#X['turnoverTime'] = X['turnoverTime'].apply(lambda x: int(x))
	Y_time = Y_time.apply(lambda x: 0 if ( int(x) <0 ) else x )#.astype(int)
	
	'''
	# Create linear regression object
	regr = linear_model.LinearRegression()

	# Train the model using the training sets
	regr.fit(fitX, Y)
	'''
	clf = svm.SVC()
	clf.fit(fitX_time, Y_time)

	joblib.dump(clf, 'time.pkl')
	joblib.dump(d, 'timed.pkl')
	
	return clf.support_vectors_.tolist() 		


def predict(input):
	
	clf_amount = joblib.load('amount.pkl')
	d = joblib.load('amountd.pkl')
	fileName = input['file']
	data = pd.read_csv(fileName)
	
	trainCols = ['company_name', 'group_key_promoters','activity_company','address_company']
	data = data[trainCols]
	data['address_company'] = data['address_company'].apply(pinCode)
	fit_amount = data.apply(lambda x: x if (x.dtype == np.float64 or x.dtype == int or x.dtype == 'datetime64') else d[x.name].fit_transform(x))
	
	# print(clf_amount.predict(fit_amount))
	


	clf_time = joblib.load('time.pkl')
	d = joblib.load('timed.pkl')
	fileName = input['file']
	data = pd.read_csv(fileName)
	trainCols = ['company_name', 'group_key_promoters','activity_company','address_company']
	data = data[trainCols]
	data['address_company'] = data['address_company'].apply(pinCode)
	fit_time = data.apply(lambda x: x if (x.dtype == np.float64 or x.dtype == int or x.dtype == 'datetime64') else d[x.name].fit_transform(x))
	
	pred_amount = clf_amount.predict(fit_amount)
	pred_time = clf_time.predict(fit_time)

	pred_times = np.ones(len(pred_time))
	for i in range(len(pred_time)):
		x = np.timedelta64(pred_time[i], 'D')
 		days = x
 		pred_times[i] = days / np.timedelta64(1, 'D')
	obj = []
	
	for i in range(len(clf_amount.predict(fit_amount))):
		obj.append({"amount": float(pred_amount[i]),"time":float(pred_times[i])})

	#print(clf_amount.predict(fit_amount).shape, )	
	#result = np.column_stack((clf_amount.predict(fit_amount),clf_time.predict(fit_time)))
	
	return obj


train({"file": "/home/pranav/Documents/my_projects/arrowAI/leadscore/leadscore_data/testdata.csv", 	"columnName" : {"amount": "amount(In Cr.)", "time": ["customer_creation_date","meeting_date" ]}	})
print(predict({"file": "/home/pranav/Documents/my_projects/arrowAI/leadscore/leadscore_data/testAmount.csv"}))

