# Monday, April 30
- First team meeting.
- Finalize the proposal.

# Wednesday, May 2
- Setup development environment and pysc2.
- Looked into game dependency trees.
- Played a few build orders to get an understanding of how the game. works.

# Saturday, May 5
- Looked into how to build order work, and how we could use the API to dynamically create a dependency tree from build command errors.

# Friday, May 11th
- Researched q learning algorithms.
- Mapped out different approaches to split the game into multiple states.
Researched game dependency trees and concluded that it’s better to use the API and q learning to test for failed build commands.   
- Looked into using actions as states to reduce the state space. By using builds as a state we can minimize the state space to only actionable states.

# Monday, May 14th
- Researched how to extract data from replays using [s2protocol](https://github.com/Blizzard/s2protocol) and [sc2Reader](https://github.com/GraylinKim/sc2reader).
- Looking at TensorFlow as a replacement to Waka.

# Saturday & Sunday, May 19-20th
- Built a python program that parses the game's replay files using [sc2Reader](https://github.com/GraylinKim/sc2reader).
- Python program to extract statistics data from multiple replay files.
- Currently extracting stats like mineral count...

# Monday May 21st
- Group meeting

# Sunday & Monday May 27-28th
- Updated stats parser
- Replay units count parser
- Looked into TenserFlow linear regression as a possible method to predict win probability.

# Fri June 1st
- Sourced replays
- Downloaded and parsed 1311 replays for unit data.

# Sat June 2nd
- Ran a linear regression over the data using TensorFlow.
- Concluded that linear regression has a low accuracy rate of 61% which is close to random of 50% accuracy.

# Mon June 4th
- Final team meeting
- Worked with Josue on using the parsed data and KNN to predict wins. 

