import networkx as nx
import matplotlib.pyplot as plt
import os
import csv

from empiricaldist import Pmf
from utils.utils import decorate
from src.ba_functions import *
from utils.graph_visualization import color_critical_nodes
from src.heuristics import critical_fraction
from src.constants import RANDOM_SEED, DATASET_PATH, FIGURES_PATH, RESULTS_PATH, DATASET_FILE_EXT, REAL_CSV_PATH, \
	BA_CSV_PATH, HK_CSV_PATH

os.makedirs(FIGURES_PATH, exist_ok=True)
os.makedirs(RESULTS_PATH, exist_ok=True)

with open(REAL_CSV_PATH, 'w', newline='') as real, \
	open(BA_CSV_PATH, 'w', newline='') as ba, \
	open(HK_CSV_PATH, 'w', newline='') as hk:

	writer1 = csv.writer(real)
	writer2 = csv.writer(ba)
	writer3 = csv.writer(hk)

	for file_path, writer in zip([REAL_CSV_PATH, BA_CSV_PATH, HK_CSV_PATH], [writer1, writer2, writer3]):
		if os.stat(file_path).st_size == 0:
			writer.writerow([
				"Graph",
				"Random Critical Fraction",
				"Targeted Critical Fraction",
				"Average Shortest Path Length",
				"Average Clustering Coefficient",
				"No. Connected Components"
			])

	for filename in os.listdir(DATASET_PATH):
		if filename.endswith(DATASET_FILE_EXT):
			dataTitle = filename[:-len(DATASET_FILE_EXT)]

			### real data
			realData = nx.read_graphml(os.path.join(DATASET_PATH, filename))
			num_nodes = realData.number_of_nodes()
			num_edges = realData.number_of_edges()
			realDegrees = dict(realData.degree())
			realDegList = list(realDegrees.values())
			realACC = nx.average_clustering(nx.Graph(realData))

			m = max(1, min(num_nodes - 1, int(round(num_edges / num_nodes))))

			### BA Graph with same number of nodes as real data, and roughly the same degree as the real data (not exact)
			baraAlbert = nx.barabasi_albert_graph(num_nodes, m, seed=RANDOM_SEED)
			bADegrees = dict(baraAlbert.degree())
			bADegList = list(bADegrees.values())
			bAACC = nx.average_clustering(nx.Graph(baraAlbert))

			### HK Graph, Same Parameters as BA
			holmesKim = nx.powerlaw_cluster_graph(num_nodes, m, realACC, seed=RANDOM_SEED)
			hKDegrees = dict(holmesKim.degree())
			hKDegList = list(hKDegrees.values())
			hkACC = nx.average_clustering(nx.Graph(holmesKim))

			### create PMFs for these
			pmf_real = Pmf.from_seq(realDegList)
			pmf_ba = Pmf.from_seq(bADegList)
			pmf_hk = Pmf.from_seq(hKDegList)

		# Get critical fraction
			realRCF, realRandNodeRemoved = critical_fraction(realData)
			realTCF, realTargetNodeRemoved = critical_fraction(realData, False)

			bARCF, bARandNodeRemoved = critical_fraction(baraAlbert)
			bATCF, bATargetNodeRemoved = critical_fraction(baraAlbert, False)

			hkRCF, hkRandNodeRemoved = critical_fraction(holmesKim)
			hkTCF, hkTargetNodeRemoved = critical_fraction(holmesKim, False)

			plt.figure(figsize=(19.2, 10.8))
			options = dict(ls='', marker='.')

			plotter(231,realData,f"Real {dataTitle}","blue",realTargetNodeRemoved)
			plotter(232,baraAlbert,f"BA {dataTitle}","purple",bATargetNodeRemoved)
			plotter(233,holmesKim,f"HK {dataTitle}","green",hkTargetNodeRemoved)

			plotter(234,pmf_real,f"PMF Real {dataTitle}","blue",probMF=True)
			plotter(235,pmf_ba,f"PMF BA {dataTitle}","purple",probMF=True)
			plotter(236,pmf_hk,f"PMF HK {dataTitle}","green",probMF=True)

			plt.savefig(f"{os.path.join(FIGURES_PATH, dataTitle)}.png")
			plt.close()

			writer1.writerow([
				dataTitle,
				realRCF,
				realTCF,
				safeASPL(realData),
				realACC,
				nx.number_connected_components(realData)
			])

			writer2.writerow([
				f"BA {dataTitle}",
				bARCF,
				bATCF,
				safeASPL(baraAlbert),
				bAACC,
				nx.number_connected_components(baraAlbert)
			])

			writer3.writerow([
				f"HK {dataTitle}",
				hkRCF,
				hkTCF,
				safeASPL(holmesKim),
				hkACC,
				nx.number_connected_components(holmesKim)
			])
