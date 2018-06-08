# Q Learning (Marine Builder bot)
Bot that tries to learn to build marines (20 in this case) as fast and as efficiently as possible.
 
## Setup
The bot is written using Python 3 and was not tested on Python 2.

#### Requirements:

- install Starcraft on any system

    - I tried using a `t2.micro` AWS EC2 Ubuntu instance to run Starcraft in headless mode but found it to be too slow with about 2 minutes per game. I then started up another `t2.2xlarge` instance that was able to run each game in about 30 seconds.

- pysc2 must be version 1.2. Later versions will not work. At the time of this writing, pip installs version 1.2.
```python
pip3 install pysc2
pip3 install pandas
```

If you do not want to train the bot but only want to run it, then you can skip to the next section section
- find where pip installed pysc2 on your machine
```python
pip3 show pysc2
```
- You need to modify the code in `run_loop.py` of pysc2 in the `env` folder
    - right before `timesteps = env.step(actions)` add 
```python
if True in actions:
break
```

This is done to force a reset from the `step()` function in the `marine_builder.py` when reaching the goal of 20 marines instead of just waiting to finish the episode. Also, it is used to break when reaching 5000 steps to speed up training.

# Running

Open `marine_builder.py` and set `RUN_TRAINED = True`. Make sure to have the `marine_builder.pkl` file in the same folder.
Then, run `train.sh` and watch the bot try to build marines if everything is good in the trained Q Table.

# Training
Open `marine_builder.py` and set `RUN_TRAINED = False`. You could have a `marine_builder.pkl` file in the same folder and the bot will load that and start training from it.
Otherwise, the bot will create a new file and start training from a fresh start.
After each game that the bot plays, it will update the `marine_builder.pkl` file. The `marine_builder.csv` is for the human to see the Q Table that the bot uses.
Run `train.sh` and watch the bot try to learn how to build marines.

# Q Table

The action space consisted of 7 actions total:
```
ACTION_DO_NOTHING,
ACTION_SELECT_SCV,
ACTION_GATHER_MINERALS,
ACTION_BUILD_SUPPLY_DEPOT,
ACTION_BUILD_BARRACKS,
ACTION_SELECT_BARRACKS,
ACTION_BUILD_MARINE
```

The state space was considerably larger:
```
marine_count,
supply_depot_count,
barracks_count,
scv_selected,
barracks_selected
```
- the combination of all of the above was much larger than anticipated because the bot kept trying to build lots of supply depots and barracks because they were easy to build
    - the built-in AI also repeatedly destroyed buildings and contributed to the state space becoming larger by allowing more variation of the current number of buildings.

# Results
After 2350 training episodes over a period of more than 24 hours, the bot did not converge on a proper sequence of building marines. When trying to run the learned Q table, the bot is not able to go past the first state because, after examining the generated Q table, the bot has incorrectly learned that selecting a barracks before one is even built leads to the highest reward.

The learning with 1536 episodes happened before the 2350 episodes and it leads to slightly better results where running the bot using just the highest Q values leads to 20 marines being built, albeit very slowly.

The improvements after the 1536 episodes seem to have made things worse for the Q learner.

#### Things tried to help the algorithm converge
- supplying a goal of 20 marines and moving to the next episode when reaching it
- supplying maximum limits of Supply Depots and Barracks and giving negative reward when going over the limit
    - also tried not allowing the bot to build past the limit in the 1536 episodes folder
- making epsilon (random choice probability) and alpha (learning rate) decrease over time instead of being constant for all of the games
    - they decrease over the course of around 400 games to their minimum values
- when reaching the goal of 20 marines, return the full reward instead of the formula for reward
- marine reward decreases over the course of each episode so more points the sooner the bot trains marines
- do not let the bot try to build barracks or supply depot if it just selected that action
    - this lets the action finish before it can be selected again
    - this is done to potentially get a direct state change based on each action since each action takes many steps to run
    - the bot is prevented from building marines but the limit is shorter than the marine build time by a factor of 4
- if an action is selected and there is no change in state, do not learn from that action
    - this should prevent actions that do not have a direct result on the state space from being given reward

# Verdict
I should have probably used a genetic algorithm to solve this problem. The state space is way too big for even building marines, a simple problem on the surface. A Q learner probably works better for things where an action has a direct result on the state space between each step, instead of having to wait hundreds of steps for that action's consequences.

A genetic algorithm could have been implemented where the gene sequence would encode actions at certain steps of the game. The actions could be the same as in this case. The fitness function would run the different actions at the specified steps and rate each gene based on how many marines it creates and how fast. To reduce the dimensionality of this problem, the generated genes could have a resolution of say 100 steps instead of choosing actions for each step. The hardest part of this algorithm would be generating the genes that encode this information and merging different genes together to make children.

Overall, this Q learner was fun to build and I have learned a lot about Q learning even though it was not as successful as I would have hoped. My expectations were too high since I thought the algorithm would figure out the optimal path on its own. By telling the algorithm more about its possible actions and defining better constraints, I still believe it may be possible to use Q learning to find the optimal path of building marines quickly.
