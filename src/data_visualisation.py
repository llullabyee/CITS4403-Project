import csv
import matplotlib.pyplot as plt
import os
import seaborn as sns
import pandas as pd
import numpy as np

from src.constants import FIGURES_VISUAL_PATH, REAL_CSV_PATH, BA_CSV_PATH, HK_CSV_PATH
from utils.graph_visualisation import cdf_plotter, hist_plotter

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



with open(REAL_CSV_PATH, 'r', newline='') as real, \
	open(BA_CSV_PATH, 'r', newline='') as ba, \
	open(HK_CSV_PATH, 'r', newline='') as hk:

	reader1 = csv.reader(real, delimiter=',')
	reader2 = csv.reader(ba, delimiter=',')
	reader3 = csv.reader(hk, delimiter=',')

	realRCF, realTCF, realASPL, realACC, realCCs = csv_reader(reader1)
	bARCF, bATCF, bAASPL, bAACC, bACCs = csv_reader(reader2)
	hkRCF, hkTCF, hkASPL, hkACC, hkCCs = csv_reader(reader3)



	### RCF
	cdf_plotter(realRCF, bARCF, hkRCF,
		    "CDF - Random Critical Fraction",
		    "Critical Fraction",
		    "Cumulative Probability")

	hist_plotter(realRCF, bARCF, hkRCF,
		     "Histogram - Random Critical Fraction",
		     "Critical Fraction",
		     "Probability Density")

	### TCF
	cdf_plotter(realTCF, bATCF, hkTCF,
		    "CDF - Targeted Critical Fraction",
		    "Critical Fraction",
		    "Cumulative Probability")

	hist_plotter(realTCF, bATCF, hkTCF,
		     "Histogram - Targeted Critical Fraction",
		     "Critical Fraction",
		     "Probability Density")

	### ASPL
	cdf_plotter(realASPL, bAASPL, hkASPL,
		    "CDF - Average Shortest Path Length",
		    "Average Shortest Path Length",
		    "Cumulative Probability")

	hist_plotter(realASPL, bAASPL, hkASPL,
		     "Histogram - Average Shortest Path Length",
		     "Shortest Path Length",
		     "Probability Density")

	### ACC
	cdf_plotter(realACC, bAACC, hkACC,
		    "CDF - Average Clustering Coefficient",
		    "Average Clustering Coefficient",
		    "Cumulative Probability")

	hist_plotter(realACC, bAACC, bAACC,
		     "Histogram - Average Clustering Coefficient",
		     "Average Clustering Coefficient",
		     "Probability Density")


	### Heatmap
	data = pd.DataFrame({
		"Network": ["Real", "BA", "HK"],
		"RCF": [np.mean(realRCF), np.mean(bARCF), np.mean(hkRCF)],
		"TCF": [np.mean(realTCF), np.mean(bATCF), np.mean(hkTCF)],
		"ASPL": [np.mean(realASPL), np.mean(bAASPL), np.mean(hkASPL)],
		"ACC": [np.mean(realACC), np.mean(bAACC), np.mean(hkACC)],
		"CCs": [np.mean(realCCs), np.mean(bACCs), np.mean(hkCCs)]
	})

	data.set_index("Network", inplace=True)

	plt.figure(figsize=(9,5))
	sns.heatmap(data, annot=True, cmap="coolwarm", fmt=".2f")
	plt.title("Network Metrics Comparison")
	plt.savefig(f"{os.path.join(FIGURES_VISUAL_PATH, "Network Metrics Comparison")}.png")
	plt.close()