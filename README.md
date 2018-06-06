# Bot-the-Builder
We plan to build a fault recovery **Bot**! *beep beep*

**Changelog**
-----
1. We are now focusing on  having the bot accomplish a goal such as build 20 marines by a certain unit of time.
2. We will be brsanching off into Q-learning ~~and the use of [Weka]~~ to determine the outcomes that a player should take.
3. We have decided to implement K-Nearest Neighbor (KNN) in order to deterimne the probability 
of a player winning at any given time. 

Methods
-----
* We plan on using **Q-learning** to teach the bot how to reach this goal.
* We run multiple iterations of the game in order to **train** the bot on the best sequence to reach this goal.
* We then **test** the bot by having it run through until it reaches its goal. 

Q-Learning
---
- We need a Q-table to store the possible actions the bot will take
- Possible actions: `build_barracks()`, `build_workers()`
- randomly select which action to take at each step 

K-Nearest Neighbor
---
* We parse over 1k replays saving at every predetermined time interval  
* We select 91 labels of interest such as *Barracks*, *BarracksTechLab*, etc. to help create the model
* The 92<sup>nd</sup> label is the win label which will be used as our Y value
* The parsed replays are dumped into a *.csv* file which are loaded into a *pandas* `DataFrame`
* The `DataFrame` is sliced to fit the requirements of **Scikit-learn's** `KNeighborsClassifier` algorithm


~~Weka~~
---
- ~~Gather large amounts of replay data~~
- ~~Determine which points of data to retrieve and dump into a csv file~~
- ~~Upload csv file to Weka GUI~~

Resources
---
* Q-learning: [Youtube video on Q-Learning](https://youtu.be/qPE4CPQY7mc), [Example using Python](http://amunategui.github.io/reinforcement-learning/), [Using Tensor Flow for Q-Learning](https://medium.com/emergent-future/simple-reinforcement-learning-with-tensorflow-part-0-q-learning-with-tables-and-neural-networks-d195264329d0), [Youtube video on Tensor flow and Q-learning](https://youtu.be/Vz5l886eptw)
* PYSC2: [Building a smart agent](https://chatbotslife.com/building-a-smart-pysc2-agent-cdc269cb095d), [building a bot](https://github.com/skjb/pysc2-tutorial)

* ~~Weka:~~ [Youtube Tutorial](https://www.youtube.com/watch?v=m7kpIBGEdkI)

* Markdown: [Md Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)
