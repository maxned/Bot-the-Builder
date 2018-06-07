# Running KNN (Python 2.x )

Libraries Needed:
---
1. `pandas`
2. `numpy`
3. `scipy`
4. `scikit-learn`
 
 These library can be installed with the *libraryInstall* script in this repo using: <br/>
 `bash libraryInstall.sh` <br/>

 Using `KNN.py`
---
1. Ensure that the csv file of the 1k parsed data is in the local folder of `KNN.py`
2. Ensure that the data for the game we are interested in determining its outcome is also in the local folder of `KNN.py`
3. Run the python file using `bash runKNN.sh`
4. The script will prompt user for name of 1k parsed file followed the a prompt asking if the 0th column of the csv file contains the index which **needs** to be ignored for KNN 
5. The scrip will continue and create **4 csv** files containing the probabilities at each time step of the replay. The difference in csv files is the number of *k* selected (5,10,15,20)

Having these four separate files gives us an insight in how there needs to be some fine tuning in determining how many neighbors we should select to make a better prediction. 



