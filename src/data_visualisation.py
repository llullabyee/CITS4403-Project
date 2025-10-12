import csv
import matplotlib.pyplot as plt
import os
import seaborn as sns
import pandas as pd
import numpy as np

from src.constants import FIGURES_VISUAL_PATH, REAL_CSV_PATH, BA_CSV_PATH, HK_CSV_PATH, REAL_GCC_PATH, BA_GCC_PATH, \
	HK_GCC_PATH
from utils.graph_visualisation import  visualize_network_metrics

os.makedirs(FIGURES_VISUAL_PATH, exist_ok=True)

def csv_reader(csvreader):
	RCF, TCF, ASPL, ACC, CCs = [], [], [], [], []
	next(csvreader)
	for row in csvreader:
		RCF.append(float(row[1]))
		TCF.append(float(row[2]))
		ASPL.append(float(row[3]))
		ACC.append(float(row[4]))
		CCs.append(float(row[5]))
	return RCF, TCF, ASPL, ACC, CCs

with open(REAL_CSV_PATH, 'r', newline='') as real_file, \
	    open(BA_CSV_PATH, 'r', newline='') as ba_file, \
	    open(HK_CSV_PATH, 'r', newline='') as hk_file:

	reader1 = csv.reader(real_file, delimiter=',')
	reader2 = csv.reader(ba_file, delimiter=',')
	reader3 = csv.reader(hk_file, delimiter=',')

	# Original / full networks
	real_data = csv_reader(reader1)
	ba_data   = csv_reader(reader2)
	hk_data   = csv_reader(reader3)

	visualize_network_metrics(real_data, ba_data, hk_data, suffix="")

	with open(REAL_GCC_PATH, 'r', newline='') as real_gcc, \
		    open(BA_GCC_PATH, 'r', newline='') as ba_gcc, \
		    open(HK_GCC_PATH, 'r', newline='') as hk_gcc:

		reader1_gcc = csv.reader(real_gcc, delimiter=',')
		reader2_gcc = csv.reader(ba_gcc, delimiter=',')
		reader3_gcc = csv.reader(hk_gcc, delimiter=',')

		real_gcc_data = csv_reader(reader1_gcc)
		ba_gcc_data   = csv_reader(reader2_gcc)
		hk_gcc_data   = csv_reader(reader3_gcc)

		visualize_network_metrics(real_gcc_data, ba_gcc_data, hk_gcc_data, suffix=" GCC")