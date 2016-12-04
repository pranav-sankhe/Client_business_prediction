import numpy as np 
import os 
import matplotlib.pyplot as plt
import pandas as pd 
import fuzzywuzzy
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from datetime import datetime
import itertools as it
#checking the type of file
path = os.getcwd() + '/testdata.csv'


def file_type():
    extension = os.path.splitext(os.path.basename(path))[1] 
    
    extensions = ['.txt', '.csv', 'xlsx' ]
    
    if extension == extensions[0]:
        return 0
    if extension == extensions[1]:
        return 1 
    if extension == extensions[2]:
        return 2 

def str2int(s, chars):
    i = 0
    for c in reversed(s):
        i *= len(chars)
        i += chars.index(c)
    return i

chars = "".join(str(n) for n in range(10)) + "ABCDEFGHIJKLMNOPQRSTUVWXYZ-"
    

def load_data():
    if file_type() == 0|1:
        data = pd.read_csv(path, delimiter=None, header='infer')

        namelist = data.columns.values.tolist()
        

        id_match = np.zeros(len(namelist))
        amount_match = np.zeros(len(namelist))
        turnoverTime_match = np.zeros(len(namelist))
        create_date_match = np.zeros(len(namelist))
        meet_date_match = np.zeros(len(namelist))
        
        for i in range(len(namelist)):
            id_match[i] = fuzz.token_set_ratio("id",namelist[i])
        
            amount_match[i] = max(fuzz.token_set_ratio("total",namelist[i]),fuzz.token_set_ratio("amount",namelist[i]))
            #turnoverTime_match = fuzz.token_set_ratio("",namelist[i])
            create_date_match[i] =  max(fuzz.token_set_ratio("creation",namelist[i]), fuzz.token_set_ratio("start",namelist[i]))
            meet_date_match[i] = max(fuzz.token_set_ratio("meeting",namelist[i]),fuzz.token_set_ratio("customer meeting",namelist[i]) )
            
            customer_id_index = np.argmax(id_match, axis=None, out=None)
            amount_index =  np.argmax(amount_match, axis=None, out=None)
            create_date_index = np.argmax(create_date_match, axis=None, out=None)
            meet_date_index = np.argmax(meet_date_match, axis=None, out=None)
            
        
        customer_id = data.iloc[:,customer_id_index:customer_id_index+1]
        amount = data.iloc[:,amount_index:amount_index+1]
        create_date =  data.iloc[:,create_date_index:create_date_index+1]
        meet_date = data.iloc[:,meet_date_index:meet_date_index+1]
        
        return customer_id, amount, create_date, meet_date,namelist



startdate_array = load_data()[2].as_matrix()
meetdate_array =  load_data()[3].as_matrix()

turnoverTime = np.zeros(len(startdate_array))


#print(startdate_array[0,:][0])


try:
    for i in range(max(len(startdate_array), len(meetdate_array) )):  
        d1 = datetime.strptime((startdate_array[i,:][0].split(" ")[0]), "%Y/%m/%d")
        d2 = datetime.strptime((meetdate_array[i,:][0]), "%Y/%m/%d")
        turnoverTime[i] = abs((d2 - d1).days)  
except AttributeError:
    pass



customer_id = load_data()[0].as_matrix() 
amount = load_data()[1].as_matrix()
amount_mean =np.mean(amount) 
amount_var = np.std(amount)
amount = (amount - np.mean(amount) )/ np.std(amount)

for i in range(len(customer_id)):
    customer_id[i] = str2int(customer_id[i,:][0], chars) 

 
customer_id = (customer_id - np.mean(customer_id)) / np.std(customer_id)

turnoverTime_mean = np.mean(turnoverTime)
turnoverTime_var = np.std(turnoverTime)
turnoverTime =  (turnoverTime - np.mean(turnoverTime)) / np.std(turnoverTime)

theta = np.matrix(np.array([0,0]))
X = np.column_stack((np.ones(len(customer_id)), customer_id) )


def computeCost(X, y, theta):                                                   
    inner = np.power(((X * theta.T) - y), 2)
    return np.sum(inner) / (2 * len(X))


 
def gradientDescent(X, y, theta, alpha, iters):  
    temp = np.matrix(np.zeros(theta.shape))
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

alpha = 0.01       #learning rate  
iters = 1000      #no. of iterations
g_turnoverTime, cost_turnoverTime = gradientDescent(X, turnoverTime, theta, alpha, iters)
g_amount, cost_amount = gradientDescent(X, amount, theta, alpha, iters)

x = np.linspace(np.amin(X[:,1]), np.amax(X[:,1]), 100)


f_turnoverTime = g_turnoverTime[0,0] + g_turnoverTime[0,1]*x
f_amount =  g_amount[0,0] + g_amount[0,0]*x  
result_turnover_time = f_turnoverTime*turnoverTime_var + turnoverTime_mean
result_amount = f_amount*amount_var + amount_mean


