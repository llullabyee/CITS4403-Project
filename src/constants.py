"""
    This module is used to set constants.
"""
import os

RANDOM_SEED = 4403

DATASET_FILE_EXT = ".graphml"
DATASET_PATH = os.path.join(os.path.dirname(__file__),'..' ,'data')
FIGURES_PATH = os.path.join(os.path.dirname(__file__),'..' ,'figures')
RESULTS_PATH = os.path.join(os.path.dirname(__file__),'..' ,'results')