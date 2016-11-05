"""
Train Input Format:
{
	"file": "data.csv",
	"predict": "Time"
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

def train(input):
	# input = {"file": "data.csv", "predict": "Time"}
	print input
	d = defaultdict(preprocessing.LabelEncoder)

	# def train(input):
	fileName = input['file']
	data = pd.read_csv(fileName)
	print data
	predictColumn = input['predict']
	trainCols = [col for col in data.columns if col not in [predictColumn]]

	X = data[trainCols]
	# fitX = X.apply(lambda x: d[x.name].fit_transform(x) )
	print X
	fitX = X.apply(lambda x: x if (x.dtype == np.float64 or x.dtype == np.int64) else d[x.name].fit_transform(x) )
	print fitX
	Y = data[predictColumn]
	print Y
	# Create linear regression object
	regr = linear_model.LinearRegression()

	# Train the model using the training sets
	regr.fit(fitX, Y)

	joblib.dump(regr, 'filename.pkl')
	joblib.dump(d, 'd.pkl')
	return regr.coef_.tolist()


def predict(input):
	# input = {"file": "test.csv"}
	d = joblib.load('d.pkl')
	regr = joblib.load('filename.pkl')

	fileName = input['file']
	data = pd.read_csv(fileName)

	fit = data.apply(lambda x: x if (x.dtype == np.float64 or x.dtype == np.int64) else d[x.name].transform(x))

	return regr.predict(fit).tolist()