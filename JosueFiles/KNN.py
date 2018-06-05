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

#this needs to be in the same folder as thr KNN.py file
game_data = pd.read_csv(os.path.join(".", "parsed_replay.csv"))
game_data = game_data.iloc[:,1:] #if we use the parsing from replay we need to
#get rid of the column that says if the game was a win or loss
#replace the value of who they played against
game_data.replace({'opponent' : { 'T' : 1, 'Z' : 2, 'P' : 3 }}, inplace =True)

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
    predictions = knn.predict_proba(game_data)
    prediction_list = []

    #predictions is formatted in a 2D array where the second value of the row is
    #the prediction of winning ie( predictions=[[0.7,0.3],[0.1,0.9]] ) where
    # the probability of winning is 0.3 and 0.9
    for i in xrange(len(predictions)):
        prediction_list.append(predictions[i][1])

    #appending a column of the predictions we are making throughout the game
    game_data['prediction'] = prediction_list
    
    #this gives us the entire average probability of the entire game winning
    #if we want to check out how well our prediction did for the whole game
    probability_of_entire_game_win = reduce(lambda x, y: x + y, prediction_list)/len(prediction_list)

    #creating a smaller dataframe that will only contain the seconds of the game
    # and the prediction for each of those time steps
    data_for_plotting = pd.DataFrame()
    data_for_plotting['seconds'] = game_data['seconds']
    data_for_plotting['prediction'] = game_data['prediction']

    # send the prediction to a CSV file with the unique name of K number of 
    #neighbors as the name of the file and removing indexes and the column names
    filename = "K_"+str(num_neighbors) + ".csv"
    data_for_plotting.to_csv(filename, index = False, header = True)



