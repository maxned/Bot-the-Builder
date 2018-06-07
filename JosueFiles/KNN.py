import pandas as pd
import requests as req
import numpy as np
import datetime
import os, sys

#importing the modules to split the data into train and test sets 
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

neighbors_values = [5,10,15,20]

#ask user for names of input files
filename1 = raw_input('Enter 1k parsed filename: ')
filename2 = raw_input('Enter single game filename: ')

# Uploading all the win/lose replays into dataframes to make it more manegable
#in this case the csv file has column 0 as the index which we will use so that 
# KNN does not use column to add to dimension
data = pd.read_csv(os.path.join(".", filename1), index_col = 0)
#data = pd.read_csv(os.path.join(".", "1Units-1311.csv"), index_col = 0)

#this needs to be in the same folder as thr KNN.py file
#in this case the csv file has column 0 as the index which we will use so that 
# KNN does not use column to add to dimension

game_data = pd.read_csv(os.path.join(".", filename2), index_col = 0)
#game_data = pd.read_csv(os.path.join(".", "parsed_replay.csv"), index_col = 0)

""" Section 1:
 Uncommet following code if there is data that has not been relabeled
in the opponent category """
#game_data = game_data.iloc[:,1:] #if we use the parsing from replay we need to
#get rid of the column that says if the game was a win or loss
#replace the value of who they played against

#game_data.replace({'opponent' : { 'T' : 1, 'Z' : 2, 'P' : 3 }}, inplace =True)

#replacing the column of oppponent from strings to ints, pretty self explanitory
#data.replace({'opponent' : { 'T' : 1, 'Z' : 2, 'P' : 3 }}, inplace =True)
"""end of Section 1 """

#we are splitting up the data into the X values and y values 
# X is the inputs which is composed of various pieces of information
#y is the output which in our case is weather the player won or lost
#X = data.iloc[:,1:]
#y = data['winner']

""" Section 2:
Following section is in case you want to split the data and see how well it scores
We have already tested our data and have an acduracy of 0.80 """
# the method train_test_split will split the dataframe into random train and test subsets 
#X_train, X_test, y_train, y_test = train_test_split(X,y, random_state = 42)
"""end of section 2 """


# KNeighborsClassifier params: 
# n_neighbors, weights, algorithm, leaf_size, p, metric, metric_params, n_jobs
# see http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html for more info on params
#

for num_neighbors in neighbors_values:
    #We need to make copies of original DF so that we don't loose the correct
    #dimensionality of the data for KNN
    parsed_Data = data.copy()
    testing_Data = game_data.copy()
    
    #will extract all rows and columns except the win column for X 
    X = parsed_Data.iloc[:,1:] 
    #will extract the win column
    y = parsed_Data['winner']

    #using mutiple values of neighbors, in this case 5, 10,15,20
    knn = KNeighborsClassifier(n_neighbors = num_neighbors)
    #fitting the data into the KNN classifier
    knn.fit(X, y)
    #creating an 2d array of predictions of each time step of the testing_Data
    predictions = knn.predict_proba(testing_Data)
    prediction_list = []

    #predictions is formatted in a 2D array where the second value of the row is
    #the prediction of winning ie( predictions=[[0.7,0.3],[0.1,0.9]] ) where
    # the probability of winning is 0.3 and 0.9
    for i in xrange(len(predictions)):
        prediction_list.append(predictions[i][1])

    #appending a column of the predictions we are making throughout the game
    testing_Data['prediction'] = prediction_list
    
    #this gives us the entire average probability of the entire game winning
    #if we want to check out how well our prediction did for the whole game
    probability_of_entire_game_win = reduce(lambda x, y: x + y, prediction_list)/len(prediction_list)
    print("Overall Win Prob of game with k=", num_neighbors, " is: ", probability_of_entire_game_win)

    #creating a smaller dataframe that will only contain the seconds of the game
    # and the prediction for each of those time steps
    data_for_plotting = pd.DataFrame()
    data_for_plotting['seconds'] = testing_Data['seconds']
    data_for_plotting['prediction'] = testing_Data['prediction']

    # send the prediction to a CSV file with the unique name of K number of 
    #neighbors as the name of the file and removing indexes and the column names
    filename = "K_"+str(num_neighbors) + ".csv"
    data_for_plotting.to_csv(filename, index = False, header = True)



