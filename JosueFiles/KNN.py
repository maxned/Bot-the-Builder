import pandas as pd
import requests as req
import numpy as np
import datetime
import os, sys

#importing the modules to split the data into train and test sets 
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

neighbors_values = [5,10,15,20]

# Uploading all the win/lose replays into dataframes to make it more manegable
data = pd.read_csv(os.path.join(".", "Units-1311.csv"))

#replacing the column of oppponent from strings to ints, pretty self explanitory
data.replace({'opponent' : { 'T' : 1, 'Z' : 2, 'P' : 3 }}, inplace =True)

#we are splitting up the data into the X values and y values 
# X is the inputs which is composed of various pieces of information
#y is the output which in our case is weather the player won or lost
X = data.iloc[:,1:]
y = data['winner']

# the method train_test_split will split the dataframe into random train and test subsets 
X_train, X_test, y_train, y_test = train_test_split(X,y, random_state = 42)

# KNeighborsClassifier params: n_neighbors, weights, algorithm, leaf_size, p, metric, metric_params, n_jobs
# see http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html for more info on params
#

for num_neighbors in neighbors_values:
    knn = KNeighborsClassifier(n_neighbors=num_neighbors)
    knn.fit(X_train, y_train)
    predictions = knn.predict_proba("INSERT GAME DATA WE WANT TO EVAL")
    
