# Bot-the-Builder
We plan to build a fault recovery **Bot**! *beep beep*

**Changelog**
-----
1. We are now focusing on  having the bot accomplish a goal such as build 20 marines by a certain unit of time.
2. We will be brsanching off into Q-learning and the use of [Weka](https://www.cs.waikato.ac.nz/ml/index.html) to determine the outcomes that a player should take.

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

Weka
---
- Gather large amounts of replay data
- Determine which points of data to retrieve and dump into a csv file
- Upload csv file to Weka GUI

Resources
---
* Q-learning: [Youtube video on Q-Learning](https://youtu.be/qPE4CPQY7mc), [Example using Python](http://amunategui.github.io/reinforcement-learning/), [Using Tensor Flow for Q-Learning](https://medium.com/emergent-future/simple-reinforcement-learning-with-tensorflow-part-0-q-learning-with-tables-and-neural-networks-d195264329d0), [Youtube video on Tensor flow and Q-learning](https://youtu.be/Vz5l886eptw)
* PYSC2: [Building a smart agent](https://chatbotslife.com/building-a-smart-pysc2-agent-cdc269cb095d), [building a bot](https://github.com/skjb/pysc2-tutorial)

* Weka: [Youtube Tutorial](https://www.youtube.com/watch?v=m7kpIBGEdkI)
