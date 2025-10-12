"""
    This module is used to set constants.
"""
import os

RANDOM_SEED = 4403


DATASET_FILE_EXT = ".graphml"
DATASET_PATH = os.path.join(os.path.dirname(__file__),'..' ,'data')
FIGURES_MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'figures', 'models')
FIGURES_VISUAL_PATH = os.path.join(os.path.dirname(__file__), '..', 'figures', 'visuals')
RESULTS_PATH = os.path.join(os.path.dirname(__file__),'..' ,'results')

REAL_CSV_PATH = os.path.join(RESULTS_PATH, 'real.csv')
BA_CSV_PATH = os.path.join(RESULTS_PATH, 'ba.csv')
HK_CSV_PATH = os.path.join(RESULTS_PATH, 'hk.csv')