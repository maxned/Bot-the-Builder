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
4. The script will prompt user for name of 1k parsed file followed the a prompt asking if the parsed file is in raw format (ie if column 0 is time step and not index)
5. The the scrip will ask user for the name of the single game replay followed by another prompt asking if it is in raw format
6. The scrip will continue and create **4 csv** files containing the probabilities at each time step of the replay. The difference in csv files is the number of *k* selected (5,10,15,20)

Example of Raw csv format:
| winner        | opponent      | seconds|
| -------------:|:-------------:| -----: |
| 0             | Z             |     0  |
| 0             | Z             |     10 |
| 0             | Z             |     15 |

Example of other acceptable csv format:
|     | winner        | opponent      | seconds|
|---  | -------------:|:-------------:| -----: |
| 97  | 0             | 1             |     0  |
| 98  | 0             | 1             |     10 |
| 99  | 0             | 1             |     15 |


Having these four separate files gives us an insight in how there needs to be some fine tuning in determining how many neighbors we should select to make a better prediction. 



