import os  
import numpy as np  
import pandas as pd  
import matplotlib.pyplot as plt


path = os.getcwd() + '/testdata.txt' 
data = pd.read_csv(path, header=1, names=['Customer_ID','Age', 'Martial status','Turnover time','Buisness amount'])           #read data from the file 
#data = pd.read_csv(path, header=1, names=['Customer_ID','company name', 'group_key_promoters','activity_company','contact_company','authorized_person_mobile','address_company','customer_creation_date','meeting_date','amount'])           #read data from the file 

#print("before normalization")
print(data.head())  #to display first few rows.

#feature(variable) normalization 

data = (data - data.mean()) / data.std()  
data.insert(0, 'Ones', 1)
print(data.mean())
print(data.std())

#print("after normalization")
print(data.head())


# set X (training data) and y (target variable)
cols = data.shape[1]  
del data['Customer_ID']
cols_update = data.shape[1]  
X = data.iloc[:,0:cols-3]  
y = data.iloc[:,cols_update-2:cols_update]

# convert to matrices and initialize theta
X = np.matrix(X.values) 
 
y = np.matrix(y.values)  
theta = np.matrix(np.array([0,0,0]))

y_turnover_time = y[:,0]
y_amount = y[:,1]

#print(np.squeeze(np.asarray(y_turnover_time)).sum())
#print(y_amount.shape)



#cost function
def computeCost(X, y, theta):                                                   
    inner = np.power(((X * theta.T) - y), 2)
    return np.sum(inner) / (2 * len(X))

def gradientDescent(X, y, theta, alpha, iters):  
    temp = np.matrix(np.zeros(theta.shape))
    
    # .ravel() flattens a matrix into a 1-D array 
    # number of parameters = parameters
    parameters = int(theta.ravel().shape[1])                                   
    cost = np.zeros(iters)

    for i in range(iters):             
        error = (X * theta.T) - y

        for j in range(parameters):
            term = np.multiply(error, X[:,j])
            temp[0,j] = theta[0,j] - ((alpha / len(X)) * np.sum(term))

        theta = temp
        cost[i] = computeCost(X, y, theta)

    return theta, cost

alpha = 0.02       #learning rate  
iters = 1000      #no. of iterations

g_turnover_time, cost_turnover_time = gradientDescent(X, y_turnover_time, theta, alpha, iters)
g_amount, cost_amount = gradientDescent(X, y_amount, theta, alpha, iters)

x_age = np.linspace(np.amin(X[:,1]), np.amax(X[:,1]), 100)
x_martialStatus = np.linspace(np.amin(X[:,2]), np.amax(X[:,2]), 100)

f_turnover_time = g_turnover_time[0,0] + g_turnover_time[0,1]*x_age + g_turnover_time[0,2]*x_martialStatus   
f_amount =  g_amount[0,0] + g_amount[0,0]*x_age + g_amount[0,0]*x_martialStatus 

#print(f_turnover_time)
#print(f_amount)
turnover = (f_turnover_time + data.mean()[3])*data.std()[3]
#amount = (f_amount + data.mean()[4])*data.std()[4]

#print(turnover)
#print(amount)



