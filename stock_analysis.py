# -*- coding: utf-8 -*-
"""Stock Analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YRGHEC10ir1YO3-s-DAFAftTJFxiby84

# ***Name: Ahmed Nasser Ahmed Hassan***
> **CodeClause |> *Sep/2022***
>> **Data Science Intern |> *CC-OL-911***
>>> **Task1 >> *Stock Analysis***
---

> ### |> ***Requirements***

>> #### |> ***Install Libraries***
"""

!pip install pandas-datareader
!pip install kaggle

""">> #### |> ***Import Packages***"""

import sys
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as data

from sklearn.preprocessing import MinMaxScaler

from keras.layers import Dense, Dropout, LSTM
from keras.models import Sequential

"""> ### |> ***Download Dataset***

>> #### |> ***Get Dataset from Kaggle with API_Token***
>> - "username":"ahmednasser1601"
>> - "key":"fd950b67a38861322900a50fdc9f6881"
"""

!mkdir ~/.kaggle
!touch ~/.kaggle/kaggle.json

api_token = {"username":"ahmednasser1601","key":"fd950b67a38861322900a50fdc9f6881"}

with open('/root/.kaggle/kaggle.json', 'w') as file:
    json.dump(api_token, file)

!chmod 600 ~/.kaggle/kaggle.json

""">> #### |> ***Download Dataset file***"""

!kaggle datasets download vijayvvenkitesh/microsoft-stock-time-series-analysis -f Microsoft_Stock.csv

dataset = pd.read_csv('Microsoft_Stock.csv')
dataset

"""---

> ### |> ***Exploring the Data***
"""

plt.plot(dataset.Close)

df = dataset.drop(['Date'], axis = 1)
df.head()

avg1 = df.Close.rolling(100).mean()   #100 Days
avg2 = df.Close.rolling(200).mean()   #200 Days

avg1

plt.figure(figsize = (16,8))
plt.plot(df.Close,'blue')
plt.plot(avg1,'red')
plt.plot(avg2,'green')

"""---

> ### |> ***Data Processing***

>> #### |> ***Splitting [Train >< Test]***
"""

trainSplit = 70/100     #Training Percentage

trainData = pd.DataFrame(df['Close'][0 : int(len(df)*trainSplit)])
testData = pd.DataFrame(df['Close'][int(len(df)*trainSplit) : int(len(df))])

print('Training', trainData.shape, '   |   ', 'Testing', testData.shape)

trainData

""">> #### |> ***Scaling [0 < Data < 1]***"""

dataScaler = MinMaxScaler(feature_range = (0, 1))

trainData_arr = dataScaler.fit_transform(trainData)

print('Training Data:', trainData_arr.shape)
trainData_arr

xTrain = []
yTrain = []

for i in range(100, trainData_arr.shape[0]):
    xTrain.append(trainData_arr[i-100 : i])
    yTrain.append(trainData_arr[i,0])
    
xTrain, yTrain = np.array(xTrain), np.array(yTrain)

"""---

> ### |> ***ML Model Building***
"""

model = Sequential()

model.add(LSTM(units = 50, activation = 'relu', return_sequences = True, input_shape = (xTrain.shape[1], 1)))
model.add(Dropout(0.2))

model.add(LSTM(units = 60, activation = 'relu', return_sequences = True))
model.add(Dropout(0.3))

model.add(LSTM(units = 80, activation = 'relu', return_sequences = True))
model.add(Dropout(0.4))

model.add(LSTM(units = 120, activation = 'relu'))
model.add(Dropout(0.5))

model.add(Dense(units = 1))

model.summary()

model.compile(optimizer = 'adam', loss = 'mean_squared_error')
model.fit(xTrain, yTrain, epochs = 100)

model.save('Model.h5')
print('Model.h5 file is saved successfully')

"""---

> ### |> ***Testing the Model***
"""

Last100Days = trainData.tail(100)
finalDF = Last100Days.append(testData, ignore_index=True)

inputData = dataScaler.fit_transform(finalDF)
inputData.shape

xTest = []
yTest = []

for i in range(100, inputData.shape[0]):
    xTest.append(inputData[i-100 : i])
    yTest.append(inputData[i, 0])

xTest, yTest = np.array(xTest), np.array(yTest)
print(xTest.shape, '   |   ', yTest.shape)

yPredict = model.predict(xTest)   #Get Predictions
yPredict.shape

dataScaler.scale_

scaleFactor = 1/0.03199539
yPredict *= scaleFactor
yTest *= scaleFactor

"""> ### |> ***Plotting [Original vs Predicted]***"""

plt.figure(figsize = (20,10))
plt.plot(yTest, 'green', label = 'Original Price')
plt.plot(yPredict, 'red', label = 'Predicted Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()

plt.show()

"""---"""