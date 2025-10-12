import networkx as nx
import matplotlib.pyplot as plt
import os
import csv

from empiricaldist import Pmf
from utils.utils import decorate
from utils.graph_visualisation import color_critical_nodes, model_plotter, plot_models
from src.heuristics import critical_fraction, safeASPL, gccSimulation, get_crit_frac
from src.constants import RANDOM_SEED, DATASET_PATH, FIGURES_MODEL_PATH, RESULTS_PATH, DATASET_FILE_EXT, REAL_CSV_PATH, \
	BA_CSV_PATH, HK_CSV_PATH, REAL_GCC_PATH, BA_GCC_PATH, HK_GCC_PATH, FIGURES_ORIGINAL_PATH, FIGURES_GCC_PATH

os.makedirs(FIGURES_MODEL_PATH, exist_ok=True)
os.makedirs(FIGURES_ORIGINAL_PATH, exist_ok=True)
os.makedirs(FIGURES_GCC_PATH, exist_ok=True)
os.makedirs(RESULTS_PATH, exist_ok=True)

with (open(REAL_CSV_PATH, 'w', newline='') as real, \
	open(BA_CSV_PATH, 'w', newline='') as ba, \
	open(HK_CSV_PATH, 'w', newline='') as hk, \
	open(REAL_GCC_PATH, 'w', newline='') as realGCC, \
	open(BA_GCC_PATH, 'w', newline='') as baGCC, \
	open(HK_GCC_PATH, 'w', newline='') as hkGCC):

	# Full Graph
	writer1 = csv.writer(real)
	writer2 = csv.writer(ba)
	writer3 = csv.writer(hk)
	#GCC only
	writer4 = csv.writer(realGCC)
	writer5 = csv.writer(baGCC)
	writer6 = csv.writer(hkGCC)

	for file_path, writer in zip([REAL_CSV_PATH, BA_CSV_PATH, HK_CSV_PATH, REAL_GCC_PATH, BA_GCC_PATH, HK_GCC_PATH],
				     [writer1, writer2, writer3, writer4, writer5, writer6]):
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
			components = list(nx.connected_components(realData))
			largest_cc = max(components, key=len)
			realDataGCC = realData.subgraph(largest_cc).copy()

			baraAlbert, holmesKim, pmf_real, pmf_ba, \
			pmf_hk, realACC, bAACC, hkACC = gccSimulation(realData)

			baraAlbertGCC, holmesKimGCC, pmf_real_gcc, \
			pmf_ba_gcc, pmf_hk_gcc, realACCGCC, baACCGCC, hkACCGCC = gccSimulation(realDataGCC)

			# Get critical fraction
			realRCF, realRandNodeRemoved, realTCF, realTargetNodeRemoved, bARCF, \
			bARandNodeRemoved, bATCF, bATargetNodeRemoved, hkRCF, hkRandNodeRemoved, \
			hkTCF, hkTargetNodeRemoved = get_crit_frac(realData, baraAlbert, holmesKim)

			realRCFGCC, realRandNodeRemovedGCC, realTCFGCC, realTargetNodeRemovedGCC, bARCFGCC, \
			bARandNodeRemovedGCC, bATCFGCC, bATargetNodeRemovedGCC, hkRCFGCC, hkRandNodeRemovedGCC, \
			hkTCFGCC, hkTargetNodeRemovedGCC = get_crit_frac(realDataGCC, baraAlbertGCC, holmesKimGCC)

			plot_configs = [
				(realData, "Real", "blue", realTargetNodeRemoved, pmf_real, True),
				(baraAlbert, "BA", "purple", bATargetNodeRemoved, pmf_ba, True),
				(holmesKim, "HK", "green", hkTargetNodeRemoved, pmf_hk, True)
			]
			gcc_configs = [
				(realDataGCC, "Real", "blue", realTargetNodeRemoved, pmf_real_gcc, True),
				(baraAlbertGCC, "BA", "purple", bATargetNodeRemoved, pmf_ba_gcc, True),
				(holmesKimGCC, "HK", "green", hkTargetNodeRemoved, pmf_hk_gcc, True)
			]

			plot_models(plot_configs, os.path.join(FIGURES_ORIGINAL_PATH, f"{dataTitle}.png"), dataTitle)
			plot_models(gcc_configs, os.path.join(FIGURES_GCC_PATH, f"{dataTitle}.png"), dataTitle)


			writers_configs = [
				# Full graphs
				(writer1, realData, "Real", realRCF, realTCF, realACC),
				(writer2, baraAlbert, "BA", bARCF, bATCF, bAACC),
				(writer3, holmesKim, "HK", hkRCF, hkTCF, hkACC),
				# GCC graphs
				(writer4, realDataGCC, "Real", realRCFGCC, realTCFGCC, realACCGCC),
				(writer5, baraAlbertGCC, "BA", bARCFGCC, bATCFGCC, baACCGCC),
				(writer6, holmesKimGCC, "HK", hkRCFGCC, hkTCFGCC, hkACCGCC)
			]

			for writer, graph, label, RCF, TCF, ACC in writers_configs:
				row_title = f"{label} {dataTitle}" if label != "Real" or graph != realData else dataTitle
				writer.writerow([
					row_title,
					RCF,
					TCF,
					safeASPL(graph),
					ACC,
					nx.number_connected_components(graph)
				])
