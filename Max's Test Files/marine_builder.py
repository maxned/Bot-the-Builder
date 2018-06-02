
import random
from math import *
import time
import pdb

import numpy as np
import pandas as pd

from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features

MARINE_GOAL = 20
BUILT_MARINE_REWARD = 100
BUILT_BARRACKS = 1

# Functions
_NO_OP = actions.FUNCTIONS.no_op.id
_SELECT_POINT = actions.FUNCTIONS.select_point.id
_BUILD_SUPPLY_DEPOT = actions.FUNCTIONS.Build_SupplyDepot_screen.id
_BUILD_BARRACKS = actions.FUNCTIONS.Build_Barracks_screen.id
_TRAIN_MARINE = actions.FUNCTIONS.Train_Marine_quick.id
#_HARVEST_GATHER = actions.FUNCTIONS.Harvest_Gather_screen.id

# Features
_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index
_HIT_POINTS = features.SCREEN_FEATURES.unit_hit_points_ratio.index
_SCREEN_HEIGHT_MAP = features.SCREEN_FEATURES.height_map.index

# Unit IDs
_TERRAN_COMMANDCENTER = 18
_TERRAN_SCV = 45
_TERRAN_SUPPLY_DEPOT = 19
_TERRAN_BARRACKS = 21
_TERRAN_MARINE = 48

# Parameters
_PLAYER_SELF = 1
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
    # ACTION_GATHER_MINERALS, this can be added later to learn to move an idle SCV to gather
    ACTION_BUILD_SUPPLY_DEPOT,
    ACTION_BUILD_BARRACKS,
    ACTION_SELECT_BARRACKS,
    ACTION_BUILD_MARINE
]

# in the future add possibility to make more SCVs

# taken from https://github.com/skjb/pysc2-tutorial/tree/master/Building%20a%20Smart%20Agent
class QLearningTable:
    def __init__(self, actions, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9):
        self.actions = actions  # a list
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)

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

        self.previous_action = None
        self.previous_state = None

        self.step_count = 0

    # work with locations relative to our base
    def transformLocation(self, x, x_distance, y, y_distance):
        if not self.base_top_left:
            return [x - x_distance, y - y_distance]
        return [x + x_distance, y + y_distance]

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

    def multidim_intersect(self, arr1, arr2):
        arr1_view = arr1.view([('',arr1.dtype)]*arr1.shape[1])
        arr2_view = arr2.view([('',arr2.dtype)]*arr2.shape[1])
        intersected = np.intersect1d(arr1_view, arr2_view)
        return intersected.view(arr1.dtype).reshape(-1, arr1.shape[1])

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

    def step(self, obs):
        super(MarineBuilder, self).step(obs)

        if obs.first():
            # check if our base is in the top left corner of the map or bottom right
            player_y, player_x = (obs.observation['minimap'][_PLAYER_RELATIVE] == _PLAYER_SELF).nonzero()
            self.base_top_left = 1 if player_y.any() and player_y.mean() <= 31 else 0

        #print(self.get_current_state(obs))

        '''
        if self.previous_action is not None:
            reward = 0
            # check here previous marine count

            self.qlearn.learn(str(self.previous_state), self.previous_action, reward, str(current_state))

        rl_action = self.qlearn.choose_action(str(current_state))
        smart_action = smart_actions[rl_action]

        self.previous_state = current_state
        self.previous_action = rl_action
        '''

        smart_action = ""
        self.step_count += 1

        if smart_action == ACTION_DO_NOTHING:
            return actions.FunctionCall(_NO_OP, [])

        elif smart_action == ACTION_SELECT_SCV or self.step_count == 200:
            unit_type = obs.observation['screen'][_UNIT_TYPE]
            unit_y, unit_x = (unit_type == _TERRAN_SCV).nonzero()

            if unit_y.any():
                # choose random SCV (can improve to prefer an idle SCV)
                i = random.randint(0, len(unit_y) - 1)
                target = [unit_x[i], unit_y[i]]
                return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])

        elif smart_action == ACTION_BUILD_SUPPLY_DEPOT or self.step_count == 500 or self.step_count == 1000 or self.step_count == 1500 or self.step_count == 2000 or self.step_count == 2500:
            if _BUILD_SUPPLY_DEPOT in obs.observation['available_actions']:
                target = self.get_placement_location(obs, SUPPLY_DEPOT_SIZE)
                if target:
                    print(target)
                    return actions.FunctionCall(_BUILD_SUPPLY_DEPOT, [_NOT_QUEUED, target])

        elif smart_action == ACTION_SELECT_BARRACKS:
            unit_type = obs.observation['screen'][_UNIT_TYPE]
            unit_y, unit_x = (unit_type == _TERRAN_BARRACKS).nonzero()

            if unit_y.any():
                # choose random barracks
                i = random.randint(0, len(unit_y) - 1)
                target = [unit_x[i], unit_y[i]]
                return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])

        elif smart_action == ACTION_BUILD_BARRACKS or self.step_count == 3000 or self.step_count == 4000 or self.step_count == 5000 or self.step_count == 6000 or self.step_count == 7000:
            if _BUILD_BARRACKS in obs.observation['available_actions']:
                target = self.get_placement_location(obs, BARRACKS_SIZE)
                if target:
                    print(target)
                    return actions.FunctionCall(_BUILD_BARRACKS, [_NOT_QUEUED, target])

        elif smart_action == ACTION_BUILD_MARINE:
            if _TRAIN_MARINE in obs.observation['available_actions']:
                return actions.FunctionCall(_TRAIN_MARINE, [_QUEUED])

        return actions.FunctionCall(_NO_OP, [])
