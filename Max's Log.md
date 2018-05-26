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
