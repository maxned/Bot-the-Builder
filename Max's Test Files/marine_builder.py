'''
Before running, make sure to add the following 2 lines in pysc2/env/run_loop.py
right before "timesteps = env.step(actions)":
if True in actions:
    break

Useful websites for information:
https://itnext.io/how-to-locate-and-select-units-in-pysc2-2bb1c81f2ad3
https://itnext.io/refine-your-sparse-pysc2-agent-a3feb189bc68
https://github.com/deepmind/pysc2/blob/master/docs/environment.md
https://steemit.com/steemstem/@cpufronz/building-a-bot-for-starcraft-ii-2-the-starcraft-ii-environment
'''

import random
from math import *
import time
import pdb
import os.path

import numpy as np
import pandas as pd

from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features

MARINE_GOAL = 20
MAX_SUPPLY_DEPOTS = 2
MAX_BARRACKS = 5

MAX_STEPS_PER_EPISODE = 5000

# Functions
_NO_OP = actions.FUNCTIONS.no_op.id
_SELECT_POINT = actions.FUNCTIONS.select_point.id
_BUILD_SUPPLY_DEPOT = actions.FUNCTIONS.Build_SupplyDepot_screen.id
_BUILD_BARRACKS = actions.FUNCTIONS.Build_Barracks_screen.id
_TRAIN_MARINE = actions.FUNCTIONS.Train_Marine_quick.id
_HARVEST_GATHER = actions.FUNCTIONS.Harvest_Gather_screen.id

# Features
_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index
_HIT_POINTS = features.SCREEN_FEATURES.unit_hit_points_ratio.index
_SCREEN_HEIGHT_MAP = features.SCREEN_FEATURES.height_map.index

# Unit IDs
_TERRAN_COMMANDCENTER = 18
_TERRAN_SCV = 45
_TERRAN_SUPPLY_DEPOT = 19
_TERRAN_BARRACKS = 21
_TERRAN_MARINE = 48
_NEUTRAL_MINERAL_FIELD = 341

# Parameters
_NOT_QUEUED = [0]
_QUEUED = [1]

# Building Sizes in pixels
SUPPLY_DEPOT_SIZE = 69
BARRACKS_SIZE = 137

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

# taken from https://github.com/skjb/pysc2-tutorial/tree/master/Building%20a%20Smart%20Agent
# originally from https://github.com/MorvanZhou/Reinforcement-learning-with-tensorflow/blob/master/contents/2_Q_Learning_maze/RL_brain.py

# make epsilon increase over time to reduce the random exploration
# make discount factor gamma increase over time until the final value
class QLearningTable:
    def __init__(self, actions, learning_rate=0.2, reward_decay=0.7, e_greedy=0.9):
        self.actions = actions  # a list
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy

    def load_table_from_file(self):
        if os.path.isfile("marine_builder.pkl"):
            self.q_table = pd.read_pickle("marine_builder.pkl")
        else:
            self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)

    def save_table_to_file(self):
        self.q_table.to_pickle("marine_builder.pkl")
        self.q_table.to_csv("marine_builder.csv")
        # also output a csv for me to look at

    def choose_action(self, observation):
        self.check_state_exist(observation)

        if np.random.uniform() < self.epsilon:
            # choose best action
            state_action = self.q_table.ix[observation, :]

            # some actions have the same value
            state_action = state_action.reindex(np.random.permutation(state_action.index))

            action = state_action.idxmax()
        else:
            # choose random action
            action = np.random.choice(self.actions)

        return action

    def learn(self, s, a, r, s_):
        # do not learn if at the same state
        #if s == s_:
            #return

        self.check_state_exist(s_)
        self.check_state_exist(s)

        q_predict = self.q_table.ix[s, a]
        q_target = r + self.gamma * self.q_table.ix[s_, :].max()

        # update
        self.q_table.ix[s, a] += self.lr * (q_target - q_predict)

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            # append new state to q table
            self.q_table = self.q_table.append(pd.Series([0] * len(self.actions), index=self.q_table.columns, name=state))

class MarineBuilder(base_agent.BaseAgent):
    def __init__(self):
        super(MarineBuilder, self).__init__()

        self.qlearn = QLearningTable(actions=list(range(len(smart_actions))))
        self.qlearn.load_table_from_file()

        self.illegal_actions = []

        self.previous_action = None
        self.previous_state = None

        self.step_count = 0
        self.total_step_count = 0

    # code taken from https://softwareengineering.stackexchange.com/questions/206298/finding-possible-positions-for-rectangle-in-a-2-d-array
    # returns a list of tuples of the coordinates that are valid by looking for zeroes in the grid
    def find_valid_locations(self, grid, height, width):
        seen = set()
        check = [(0, 0, 0, 0)]
        w = width
        h = height
        items = list()
        while check:
            x, y, ox, oy = check.pop()
            if (x, y) in seen:
                continue
            seen.add((x, y))
            if x + w >= len(grid) or y + h >= len(grid[0]):
                continue
            for i, row in enumerate(grid[x+ox:x+w+1], x+ox):
                for j, val in enumerate(row[y+oy:y+h+1], y+oy):
                    if val:
                        break
                else:
                    continue
                check.extend([(i+1, y, 0, 0), (x, j+1, 0, 0)])
                break
            else:
                items.append((x,y))
                #yield (x, y)
                check.extend([(x+1, y, w-1, 0), (x, y+1, 0, h-1)])
                continue
        return items

    # returns a tuple of the best location for a unit of any size on the current screen
    def get_placement_location(self, obs, size):
        unit_type = obs.observation['screen'][_UNIT_TYPE] # returns 0 for a pixel if no unit there

        screen_height = obs.observation['screen'][_SCREEN_HEIGHT_MAP]
        screen_height[screen_height == 0] = -1 # change all zeroes to -1 because 0 is invalid location
        screen_height[screen_height > 0] = 0 # change all valid locations to 0 for find_valid_location algorithm

        non_overlapping_unit_locations = self.find_valid_locations(np.transpose(unit_type), ceil(sqrt(size)), ceil(sqrt(size)))
        valid_screen_height_locations = self.find_valid_locations(np.transpose(screen_height), ceil(sqrt(size)), ceil(sqrt(size)))
        possible_locations = list(set(non_overlapping_unit_locations) & set(valid_screen_height_locations)) # find intersection of both lists for valid locations

        if not possible_locations:
            return None

        target = random.choice(possible_locations)
        x = target[0] + round(sqrt(size)/2) # change from left corner to center of unit
        y = target[1] + round(sqrt(size)/2)
        return (x, y)

    def get_current_state(self, obs):
        marine_count = obs.observation['player'][8] 

        unit_type = obs.observation['screen'][_UNIT_TYPE]
        unit_hp = obs.observation['screen'][_HIT_POINTS]

        depot_y, depot_x = (unit_type == _TERRAN_SUPPLY_DEPOT).nonzero()
        #supply_depot_count = int(round(len(depot_y) / 69))
        supply_depot_hp = unit_hp[depot_y, depot_x] # 2d array with hp from 0 - 255 indicating the hp of that pixel for the supply depot, length of depot_hp is 69
        supply_depot_count = int(np.count_nonzero(supply_depot_hp == 255) / SUPPLY_DEPOT_SIZE) # counts number of supply depots with full health

        barracks_y, barracks_x = (unit_type == _TERRAN_BARRACKS).nonzero()
        #barracks_count = int(round(len(barracks_y) / 137))
        barracks_hp = unit_hp[barracks_y, barracks_x] # 2d array with hp from 0 - 255 indicating the hp of that pixel for the barrack, length of barracks_hp is 137
        barracks_count = int(np.count_nonzero(barracks_hp == 255) / BARRACKS_SIZE) # counts number of barracks with full health

        # check what unit is currently selected
        if len(obs.observation['single_select']) > 0 and obs.observation['single_select'][0][0] == _TERRAN_SCV:
            scv_selected = 1
            barracks_selected = 0
        elif len(obs.observation['single_select']) > 0 and obs.observation['single_select'][0][0] == _TERRAN_BARRACKS:
            scv_selected = 0
            barracks_selected = 1
        else:
            scv_selected = 0
            barracks_selected = 0

        current_state = [
            marine_count,
            supply_depot_count,
            barracks_count,
            scv_selected,
            barracks_selected,
        ]

        return current_state

    def get_reward(self, current_state, previous_state):
        # marine reward will be highest in the beginning of the episode
        # only add reward if we built a unit (if a unit is destroyed do not add negative reward)
        if (current_state[0] > previous_state[0]): # average game is around 2000 steps so reward is about 2.something points
            marine_reward = (current_state[0] - previous_state[0]) * (MAX_STEPS_PER_EPISODE / (self.step_count + 1)) # do not divide by zero
        else:
            marine_reward = 0
        
        if (current_state[1] > MAX_SUPPLY_DEPOTS):
            supply_depot_reward = -1
        else:
            supply_depot_reward = 0

        if (current_state[2] > MAX_BARRACKS):
            barracks_reward = -1
        else:
            barracks_reward = 0

        total_reward = marine_reward + supply_depot_reward + barracks_reward

        # if we move the map then return to the same spot, the previous state and current will be different
        # resulting in a negative reward being possible
        if total_reward > 0:
            return total_reward
        else:
            return 0
    
    def finished_episode(self, current_state):
        self.qlearn.save_table_to_file()
        self.illegal_actions = []
        self.step_count = 0 # reset steps at beginning of episode
        print("Finished with state")
        print(current_state)
        print(self.step_count)
        print()

    def step(self, obs):
        super(MarineBuilder, self).step(obs)            

        current_state = self.get_current_state(obs)

        if current_state[1] > MAX_SUPPLY_DEPOTS and ACTION_BUILD_SUPPLY_DEPOT not in self.illegal_actions:
            self.illegal_actions.append(ACTION_BUILD_SUPPLY_DEPOT)
        
        if current_state[2] > MAX_BARRACKS and ACTION_BUILD_BARRACKS not in self.illegal_actions:
            self.illegal_actions.append(ACTION_BUILD_BARRACKS)
        
        if self.previous_action is not None and self.previous_state is not None:
            reward = self.get_reward(current_state, self.previous_state)
            self.qlearn.learn(str(self.previous_state), self.previous_action, reward, str(current_state))

        if obs.last():
            self.finished_episode(current_state)

        unit_type = obs.observation['screen'][_UNIT_TYPE]

        # check the number of marines and end episode if reached goal
        # or if reached step_count of current episode
        # or if command center was destroyed since we will not build one again
        unit_y, _ = (unit_type == _TERRAN_COMMANDCENTER).nonzero()
        if current_state[0] >= MARINE_GOAL or self.step_count == MAX_STEPS_PER_EPISODE or not unit_y.any():
            self.finished_episode(current_state)
            # reached goal so reset
            return True

        rl_action = self.qlearn.choose_action(str(current_state))
        smart_action = smart_actions[rl_action]

        if smart_action in self.illegal_actions:
            smart_action = ACTION_DO_NOTHING

        self.previous_state = current_state
        self.previous_action = rl_action

        self.step_count += 1
        self.total_step_count += 1

        if smart_action == ACTION_DO_NOTHING:
            return actions.FunctionCall(_NO_OP, [])

        elif smart_action == ACTION_SELECT_SCV:
            unit_y, unit_x = (unit_type == _TERRAN_SCV).nonzero()

            if unit_y.any():
                # choose random SCV (can improve to prefer an idle SCV)
                i = random.randint(0, len(unit_y) - 1)
                target = [unit_x[i], unit_y[i]]
                return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])

        elif smart_action == ACTION_GATHER_MINERALS:
            if _HARVEST_GATHER in obs.observation['available_actions']:
                unit_y, unit_x = (unit_type == _NEUTRAL_MINERAL_FIELD).nonzero()
                if unit_y.any():
                    i = random.randint(0, len(unit_y) - 1)
                    m_x = unit_x[i]
                    m_y = unit_y[i]
                    target = [int(m_x), int(m_y)]
                    return actions.FunctionCall(_HARVEST_GATHER, [_QUEUED, target])

        elif smart_action == ACTION_BUILD_SUPPLY_DEPOT:
            if _BUILD_SUPPLY_DEPOT in obs.observation['available_actions']:
                target = self.get_placement_location(obs, SUPPLY_DEPOT_SIZE)
                if target:
                    return actions.FunctionCall(_BUILD_SUPPLY_DEPOT, [_NOT_QUEUED, target])

        elif smart_action == ACTION_SELECT_BARRACKS:
            unit_y, unit_x = (unit_type == _TERRAN_BARRACKS).nonzero()

            if unit_y.any():
                # choose random barracks (change later to choose the most available one)
                i = random.randint(0, len(unit_y) - 1)
                target = [unit_x[i], unit_y[i]]
                return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])

        elif smart_action == ACTION_BUILD_BARRACKS:
            if _BUILD_BARRACKS in obs.observation['available_actions']:
                target = self.get_placement_location(obs, BARRACKS_SIZE)
                if target:
                    return actions.FunctionCall(_BUILD_BARRACKS, [_NOT_QUEUED, target])

        elif smart_action == ACTION_BUILD_MARINE:
            if _TRAIN_MARINE in obs.observation['available_actions']:
                return actions.FunctionCall(_TRAIN_MARINE, [_QUEUED])

        return actions.FunctionCall(_NO_OP, [])
