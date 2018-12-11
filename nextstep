import pandas as pd
import numpy as np
import sys
import scipy
import sklearn
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from datetime import datetime
import tensorflow as tf
from tensorflow.keras import layers
from sklearn import svm, grid_search, datasets
from numpy import genfromtxt
import matplotlib.pyplot as plt

patients = pd.read_csv("patientData.csv")


print(patients.head())

patients.hist()
plt.show()

#values = {'BEHAVIOR': "Appropriate" , 'TOBACCO_HIST': "Never used"}



#patients = patients.fillna(value = values)


#Tobacco History: Never used, Former user - stopped more than 1 year ago, Stopped more than 1 month ago, but less than 1 year ago,
#Current use or use within 1 month of admission, 

#tobaccoToNum = {"Never used": 0, "Former user - stopped more than 1 year ago": 1,
#               "Stopped more than 1 month ago, but less than 1 year ago": 2,
#               "Current use or use within 1 month of admission":3,"Appropriate": 0, "Sleeping/Sedated": 1, "Sleeping":2, "Combative":3, "Confused":4, "Anxious":5, "Restless":6,
#"Withdrawn":7, "Labile":8, "Uncooperative":9, "Angry":10, "Apprehensive":11, "Delirium":12, "Apathy":13, "F":0, "M":1}


#patients = patients.replace(tobaccoToNum)

plt.figure()

#x = patients['LOS']
#y = patients['AGE']

cols = patients.columns.values
cols = np.delete(cols,0)
cols = np.delete(cols,0)
cols = np.delete(cols,17)



for column in cols:
    plt.scatter(patients[column],patients['LOS'])
    plt.ylabel('LOS')
    plt.xlabel(column)
    plt.show() # Depending on whether you use IPython or interactive mode, etc.

patients['AGE'].plot()

patients = patients.astype(float)

print(patients.dtypes)



from keras.models import Sequential
from keras.layers import Dense
import numpy
# fix random seed for reproducibility
numpy.random.seed(7)

# load pima indians dataset
dataset = numpy.loadtxt("patientData.csv", delimiter=",", skiprows = 1)
# split into input (X) and output (Y) variables
X = dataset[:,2:19]
Y = dataset[:,19]


model = Sequential()
model.add(Dense(12, input_dim=17, kernel_initializer='normal', activation='relu'))
#model.add(Dense(17, kernel_initializer='normal', activation='relu'))
model.add(Dense(1, kernel_initializer='normal'))

model.compile(loss='MSE', optimizer='adam', metrics=['MAE'])
model.fit(X, Y, epochs=150, batch_size=10)

# evaluate the model
scores = model.evaluate(X, Y)
print("\n%s: %.2f" % (model.metrics_names[1], scores[1]))
