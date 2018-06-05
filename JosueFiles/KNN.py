import pandas as pd
import os
import requests as req
#import json
import numpy as np
import datetime
#from matplotlib import style
#import matplotlib
#%matplotlib inline
#style.use('ggplot')

import os, sys

# Uploading all the win/lose replays into dataframes to make it more manegable
data1 = pd.read_csv(os.path.join("..","winreplay.csv")) 
data2 = pd.read_csv(os.path.join("..","lossreplay.csv")) 

#appending the column of win and lose to the datasets 1 being a winning 
#dataset and 0 being a losing dataset
data1['win'] = 1
data2['win'] = 0

#concatinating both wins and loses into one big dataframe 
frames = [data1, data2]
data = pd.concat(frames)

#importing the modules to split the data into train and test sets 
from sklearn.model_selection import train_test_split

#currently the dataframe has six columns, with the last column being the win/lose 
#column. For this step X gets the number of columns up to the win/lose column
# the number of columns we add to X depends on how many features we plan to obeserve
# y gets the win/lose column 
X = data.iloc[:,0:5]
y = data['win']

# the method train_test_split will split the dataframe into random train and test subsets 
X_train, X_test, y_train, y_test = train_test_split(X,y, random_state = 42)

#Now to import the KN classifier from sklearn
from sklearn.neighbors import KNeighborsClassifier

# KNeighborsClassifier params: n_neighbors, weights, algorithm, leaf_size, p, metric, metric_params, n_jobs
# see http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html for more info on params
#
# We will be changing the amount of neihbors to plot the difference in selecting the amount of neighbors
knn = KNeighborsClassifier(n_neighbors=5)

#Fit the model using X as training data and y as target values
knn.fit(X_train, y_train)

#optional
#Score our KNN to determine if we may have to either increase or decrease the number of neighbors used
knn.score(X_test, y_test)

#this will give an array of the predictions ie. [1,1,1,0,1,0] where one is win and 0 is lose
#knn.predit(data_to_predict)

#This is the function we will use to determine the probability of winning or losing
#knn.predict_proba(data_of_state)