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
1. Ensure that `"Units-1311.csv"` file which contains over 1k parsed replays is in the same directory as `KNN.py`
2. Ensure that `"parsed_replay.csv"` file is is the replay which we plan to evaluate is also in the same directory
3. Run the python file using `bash runKNN.py` which will automatically run the python script and create **4 csv** files containing the probabilities at each time step of the replay. The difference in csv files is the number of *k* selected, giving us a view of the poetential for including too many or too little neighbors in making a prediction. 



