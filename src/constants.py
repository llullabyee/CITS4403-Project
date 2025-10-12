"""
    This module is used to set constants.
"""
import os

RANDOM_SEED = 4403


DATASET_FILE_EXT = ".graphml"
DATASET_PATH = os.path.join(os.path.dirname(__file__),'..' ,'data')
FIGURES_MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'figures', 'models')
FIGURES_ORIGINAL_PATH = os.path.join(os.path.dirname(__file__), '..', 'figures', 'models', 'original')
FIGURES_GCC_PATH = os.path.join(os.path.dirname(__file__), '..', 'figures', 'models', 'gcc')
FIGURES_VISUAL_PATH = os.path.join(os.path.dirname(__file__), '..', 'figures', 'data visualisation')
RESULTS_PATH = os.path.join(os.path.dirname(__file__),'..' ,'results')
REAL_CSV_PATH = os.path.join(RESULTS_PATH, 'real.csv')
REAL_GCC_PATH = os.path.join(RESULTS_PATH, 'real_gcc.csv')
BA_CSV_PATH = os.path.join(RESULTS_PATH, 'ba.csv')
BA_GCC_PATH = os.path.join(RESULTS_PATH, 'ba_gcc.csv')
HK_CSV_PATH = os.path.join(RESULTS_PATH, 'hk.csv')
HK_GCC_PATH = os.path.join(RESULTS_PATH, 'hk_gcc.csv')