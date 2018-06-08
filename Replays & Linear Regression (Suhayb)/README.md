# Replay Parser
This parser was designed to extract specific data from Starcraft 2's replay files for Machine learning.

Dependencies
---
1. `tqdm`
2. `sc2reader`

 Dependencies can be installed by running `bash dependencies.sh`

Replay Requirement
---
- 1 vs 1 competitive games with only 2 players
- One player must select the Terran race

# Units Parser `units.py`
The parser takes in Starcraft 2 replays and extracts critical *Terran* unit data and stores the results in a .CSV file. The resulting data also includes information about the opponent and whether the player won the game or not.

Running
---
1. Install dependencies by running `bash dependencies.sh`
2. To run the parser `python3 units.py <path to the folder containing .SC2Replay>`
3. The parsed results will be stored in *output/units/*

# Stats Parser `stats.py`
The parser takes in Starcraft 2 replays and extracts critical *Terran* game statistics data and stores the results in a .CSV file.

Running
---
1. Install dependencies by running `bash dependencies.sh`
2. To run the parser `python3 stats.py <file-1.SC2Replay> <file-2.SC2Replay> ... <file-n.SC2Replay>`
3. The parsed results will be stored in *output/stats/*

___

# Linear Regression using TensorFlow `ML.py`
In order to experiment with the parsed data, we ran a linear regression over the data which resulted in a *60% accuracy* when predicting whether a state would result in a win or a loss. **From our experience Linear regression is not recommended** due to its low accuracy rate when compared to K-nearest neighbors approach.

Running
---
1. [Install TensorFlow](https://www.tensorflow.org/install/)
2. Store the source data will be read from data/Units-1311.csv
3. Run `python3 ML.py`
