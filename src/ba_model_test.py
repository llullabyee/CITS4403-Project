import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import os
from empiricaldist import Pmf
from utils.utils import decorate
from src.ba_functions import *
from utils.graph_visualization import color_critical_nodes
from src.heuristics import critical_fraction
from src.constants import RANDOM_SEED, DATASET_PATH, FIGURES_PATH, RESULTS_PATH, DATASET_FILE_EXT


os.makedirs(FIGURES_PATH, exist_ok=True)
os.makedirs(RESULTS_PATH, exist_ok=True)

rows = []

for filename in os.listdir(DATASET_PATH):
	if filename.endswith(DATASET_FILE_EXT):
		### real data
		realData = nx.read_graphml(os.path.join(DATASET_PATH, filename))
		num_nodes = realData.number_of_nodes()
		num_edges = realData.number_of_edges()
		realDegrees = dict(realData.degree())
		realDegList = list(realDegrees.values())


		### BA Graph with same number of nodes as real data, and roughly the same degree as the real data (not exact)
		m = max(1, min(num_nodes - 1, int(round(num_edges / num_nodes))))
		baraAlbert = nx.barabasi_albert_graph(num_nodes, m, seed=RANDOM_SEED)
		bADegrees = dict(baraAlbert.degree())
		bADegList = list(bADegrees.values())

		### create PMFs for these
		pmf_real = Pmf.from_seq(realDegList)
		pmf_ba = Pmf.from_seq(bADegList)
		
        # Get critical fraction
		realRCF, realRandNodeRemoved = critical_fraction(realData)
		realTCF, realTargetNodeRemoved = critical_fraction(realData, False)
		bARCF, bARandNodeRemoved = critical_fraction(baraAlbert)
		bATCF, bATargetNodeRemoved = critical_fraction(baraAlbert, False)

		plt.figure(figsize=(19.2, 10.8))
		options = dict(ls='', marker='.')

		plt.subplot(2, 2, 1)
		realData_colorMap = color_critical_nodes(realData, realTargetNodeRemoved, "skyblue")
		nx.draw(realData, node_size=20, node_color=realData_colorMap, edge_color="gray", with_labels=False)
		plt.title(filename)

		plt.subplot(2, 2, 2)
		bA_colorMap = color_critical_nodes(baraAlbert, bATargetNodeRemoved, "purple")
		nx.draw(baraAlbert, node_size=20, node_color=bA_colorMap, edge_color="gray", with_labels=False)
		plt.title(f"BA {filename}")

		plt.subplot(2, 2, 3)
		pmf_real.plot(label=filename, color='C0', **options)
		decorate(xscale='log', yscale='log',xlim=[1, 1e4],xlabel='Degree',ylabel='PMF')
		plt.title(f"PMF {filename}")

		plt.subplot(2, 2, 4)
		pmf_ba.plot(label=f"BA {filename}", color='C1', **options)
		decorate(xscale='log',yscale='log',xlim=[1, 1e4],xlabel='Degree',ylabel='PMF')
		plt.title(f"PMF BA {filename}")

		plt.savefig(f"{os.path.join(FIGURES_PATH, filename)}.png")

		rows.append({
			'Graph': filename,
			'Random_f_c': realRCF,
			'Targeted_f_c': realTCF,
			'Avg Shortest Path Length': safeASPL(realData),
			'No. of Components': nx.number_connected_components(realData)
		})

		rows.append({
			'Graph': f" BA {filename}",
			'Random_f_c': bARCF,
			'Targeted_f_c': bATCF,
			'Avg Shortest Path Length': safeASPL(baraAlbert),
			'No. of Components': nx.number_connected_components(baraAlbert)
		})

df = pd.DataFrame(rows)
df.to_csv(f'{os.path.join(RESULTS_PATH, "simulated_data.csv")}', index=False)
print(df)
