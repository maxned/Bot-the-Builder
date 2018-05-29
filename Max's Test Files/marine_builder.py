
import random
import math
import time

import numpy as np
import pandas as pd

from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features

MARINE_GOAL = 20

_NO_OP = actions.FUNCTIONS.no_op.id

_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index

ACTION_DO_NOTHING = 'donothing'
ACTION_SELECT_SCV = 'selectscv'
ACTION_GATHER_MINERALS = 'scvgatherminerals'
ACTION_BUILD_SUPPLY_DEPOT = 'buildsupplydepot'
ACTION_BUILD_BARRACKS = 'buildbarracks'
ACTION_SELECT_BARRACKS = 'selectbarracks'
ACTION_BUILD_MARINE = 'buildmarine'

smart_actions = [
    ACTION_DO_NOTHING,
    ACTION_SELECT_SCV,
    ACTION_GATHER_MINERALS,
    ACTION_BUILD_SUPPLY_DEPOT,
    ACTION_BUILD_BARRACKS,
    ACTION_SELECT_BARRACKS,
    ACTION_BUILD_MARINE,
]

# in the future add possibility to make more SCVs

marine_count = 0
state_space = [
    marine_count,
    supply_depot_count,
    barracks_count,
    scv_selected,
    barracks_selected,
]

class MarineBuilder(base_agent.BaseAgent):
    def __init__(self):
        super(MarineBuilder, self).__init__()

    def step(self, obs):
        super(MarineBuilder, self).step(obs)

        time.sleep(1)

        print(obs.observation['screen'][_UNIT_TYPE])

        return actions.FunctionCall(_NO_OP, [])
