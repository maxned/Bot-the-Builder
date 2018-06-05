# Josue Aleman
**May 29th 2018 update** <br/>
<br/>
**Log:** https://github.com/maxned/Bot-the-Builder/blob/master/Josue's%20Log.md 
<br/>
**Commits:**
- https://github.com/maxned/Bot-the-Builder/commit/bb5470bb694ffccde049ad1951064066e9d42a63

**Description:**
<br/>
<br/>
Created the model to implement the K Nearest Neighor algorithm for our project. This will read in from the win/lose folders that **@Suhayb** has created by the use of the parser he made. These folders will contain multiple games woth their state at certain time steps. We will be limiting the type of player to **Terran** due to time constraints. It will then load the win/loss data into a `pandas DataFrame`. Using Scikit-learn's KNN algorithm we have ability to recieve input (ie the state of the game) and ouput the probability of the current state being on the winning track based on the previous data loaded to the model.   