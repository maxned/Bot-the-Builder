# Saturday May 4
 - looked into the  CommandCenter bot
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
