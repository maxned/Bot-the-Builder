# Thursday June 7
- ran 2350 episodes with some new things to help the algorithm converge but the Q learner did not end up learning how to make marines quickly and efficiently
    - some things I tried were making the alpha (learning rate) and epsilon (random action chance) decrease over time so that the algorithm could randomly learn how to build marines and then converge to a steady state
    - I also tried giving the algorithm a full reward when reaching 20 marines
    - Finally, I fixed a learning bug where the previous action and state would carry over from the previous game
- Even with all of these improvements, running the Q learner just based on the best action at each state, does not get past the first step of the game because the Q learner passed down the wrong action to the start of the game, meaning it did not converge properly but relied on random actions getting it out of bad states

# Wednesday June 6
- worked on improving the learning algorithm to learn better
    - ran the algorithm overnight for 1536 games but it was very slow and inefficient at building units
    - the algorithm is still limited from building units too quickly (this is worse in real life because you could start building things at the same time but it should improve the learning to explore less and stop calling the same action)
        - this could be fixed if the algorithm could independently decide on which unit to select and can check if a unit is being built and its progress but this would make the state space much bigger

# Tuesday June 5
- spent the day trying to improve the q learning to help the algorthm to converge
- setup a new linux server on AWS to hopefully increase the training speed
- worked on reducing the state space to make convergence possible by limiting the total number of units that can be built of a certain type
- now realize a genetic algorithm may have been better than the q learning because it is easier to represent the large state and action space
    - with a genetic algorithm, the gene space might be the order that units are built in and the fitness function may be how fast that gene reached a goal of building 20 marines
    - that way, it would have been easier to converge to a good gene instead of basically having to explore a large state space with the q learner
    - the state space in the genetic algorithm would not matter (just the final result of the number of marines would dictate how well that gene is)

# Monday June 4
- Q learning bot is now able to make marines and trains itself
    - `marine_builder.csv` holds the q table in a human readable format while the `marine_builder.pkl` holds the q table for the algorithm
    - q table is saved at the end of each game so it is possible to interrupt the learning and continue from where it left off
    - just run the `train.sh` script to run and train the bot

# Sunday June 3
- worked on making it possible to reset the game early
    - this took a lot of trial and error to come to my simple solution
    - I had to run through the source code of pysc2 and figure out where to change code to handle this

- to run my source code file `marine_builder.py` you need to modify the code in `run_loop.py` of pysc2 in the `env` folder
    - right before `timesteps = env.step(actions)` add 
    ```python
     if True in actions:
        break
    ```

# Friday June 1
- finished the state space for the q learner
    - currently it includes the current number of marines, current supply depots and barracks with 100% health, and whether an scv or barracks is selected
- finished the action space for the q learner
    - possible actions are nothing, select scv or barracks, and build barracks, supply depot, or marine.
    - the locations for barracks and supply depot are smartly chosen to be placed in a valid location based on whether there are any units there, or it is a valid height in the map.
        - this is done to minimize invalid placements while still allowing for a lot of buildings to be built

# Monday May 28
- started work on my marine builder using Q-Learning
    - defined the state and action space

# Thursday May 24
- created another AWS Ubuntu instance and was able to get starcraft running in headless mode
    - this is really good because now I can train my Q-Learner

# Monday May 21
- created an Amazon EC2 Linux instance to try to get Starcraft II running in headless mode
    - installed pysc2 and the required dependencies but was not able to launch a bot due to the webscoket connection timing out
    - found a resource that used Google Collab for this purpose [here](https://medium.com/@n0mad/how-i-trained-starcraft-2-ais-using-googles-free-gpus-44bc635b0418)

# Monday May 14
- instead of trying to make a Q-Learning algorithm to create marines first in the whole game, it will be much easier to do so in a mini game by deepmind as detailed [here](https://github.com/deepmind/pysc2/blob/master/docs/mini_games.md#buildmarines)
    - this will make it much easier to test the algorithm and make sure everything is working before trying it on the actual game
    - using the knowledge from this mini game, it will be possible to extend it to the whole game to help one play the actual game

# Sunday May 13
- continued exploring the Q-learning algorithm
    - understand dimensionality reduction with a [good example](https://dev.to/n1try/cartpole-with-q-learning---first-experiences-with-openai-gym)
    - played around with [Open AI Gym](http://gym.openai.com) Cartpole example as outlined above
    - added the cartpole solving file I was learning from into the folder "Max's Test Files"
- also found a different library for sc2 that works with python, [might be useful](https://github.com/Dentosal/python-sc2)

- current plan is to implement the Q-Learning algorithm for creating units such as marines as fast as possible
    - plan for dimensionality reduction is to have a limited number of actions such as (build_barracks(), build_marine(), build_scv, build_scv(), wait_mineral_production()) and for the current state to be the number of units of each type that are currently built.
    - the learning space will be decently large but the algorithm that the AI comes up with will be interesting
    - for further dimensionality reduction, we can reduce the step rate

# Thursday May 10
- learned about the Q-Learning algorithm
    - I now understand it much better
    - followed Josue's markup as well as [this tutorial](http://mnemstudio.org/path-finding-q-learning-tutorial.htm) which was very helpful in making the algorithm more clear

# Saturday May 4
 - looked into the CommandCenter bot
    - it can build things in a build order but we do not want to use its system
    - we are trying to make our own system that will be able to backtrack and decide on what to build next
- installed the s2client-api (using Xcode) and went through the tutorials to build simple bots
    - I am thinking maybe we should switch over to making our bot in C++ because the environment and API are easier to use than in pysc2
    - a benefit of pysc2 is that it is easier to implement machine learning type algorithms
- pysc2 examples are [here](https://github.com/skjb/pysc2-tutorial)
- s2client-api information is [here](https://github.com/Blizzard/s2client-api/blob/master/docs/building.md)

# Thursday May 3
 - installed pysc2 and followed the tutorial [here](https://chatbotslife.com/building-a-basic-pysc2-agent-b109cde1477c) to get a simple bot running in the game
 - still trying to understand how the game works but the gist of it is that the game works in steps and in each step the bot can perform certain actions
 - things we need to do are build a build order system that will execute actions when it can
