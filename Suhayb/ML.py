# based off of https://github.com/tensorflow/models/blob/master/official/wide_deep/wide_deep.py

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import shutil
import tensorflow as tf

import logging
logging.getLogger().setLevel(logging.INFO)

_CSV_COLUMNS = [
   'winner','opponent','seconds','BarracksTechLab','Hellion','MULE','VikingFighter','Barracks','SiegeTankSieged','Ghost','SupplyDepot','Factory','AutoTurret','TechLab','ReaperPlaceholder','OrbitalCommandFlying','Reactor','FusionCore','Raven','Bunker','FactoryTechLab','CommandCenterFlying','VikingAssault','EngineeringBay','SiegeTank','StarportFlying','Battlecruiser','Armory','Refinery','Marine','CommandCenter','PlanetaryFortress','GhostAcademy','Thor','HellionTank','Banshee','SCV','WidowMine','FactoryReactor','Medivac','Reaper','FactoryFlying','OrbitalCommand','BarracksFlying','WidowMineBurrowed','SupplyDepotLowered','MissileTurret','Starport','Nuke','StarportTechLab','StarportReactor','SensorTower','Marauder','BarracksReactor','PointDefenseDrone'
]

_CSV_COLUMN_DEFAULTS = [[0],[''],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]]

_TRAIN_EXAMPLE_COUNT = 485108

_NUM_CPUS = 4
_DATA_DIR = 'data/Units-1311.csv'
_MODEL_DIR = 'model/'
_EPOCHS_BETWEEN_EVALS = 2
_BATCH_SIZE = 40

def inputData(dataFile, numEpochs, shuffle, batchSize):
   def parseCSV(value):
      columns = tf.decode_csv(value, record_defaults=_CSV_COLUMN_DEFAULTS)
      features = dict(zip(_CSV_COLUMNS, columns))
      labels = features.pop('winner')
      return features, tf.equal(labels, 1)

   dataset = tf.data.TextLineDataset(dataFile).skip(1)

   if shuffle:
      dataset = dataset.shuffle(buffer_size=_TRAIN_EXAMPLE_COUNT)
   dataset = dataset.map(parseCSV, num_parallel_calls=_NUM_CPUS)
   dataset = dataset.repeat(numEpochs)
   dataset = dataset.batch(batchSize)
   return dataset


opponent = tf.feature_column.categorical_column_with_vocabulary_list('opponent', ['T', 'P', 'Z'])
numColmn = [tf.feature_column.numeric_column(key=cl, dtype=tf.int32) for cl in _CSV_COLUMNS if cl !='opponent' and cl !='winner']
features = numColmn + [opponent]

model = tf.estimator.LinearClassifier(model_dir=_MODEL_DIR, feature_columns=features,
    optimizer=tf.train.FtrlOptimizer(
        learning_rate=0.1,
        l1_regularization_strength=1.0,
        l2_regularization_strength=1.0))

model.train(input_fn=lambda: inputData(_DATA_DIR, _EPOCHS_BETWEEN_EVALS, True, _BATCH_SIZE))