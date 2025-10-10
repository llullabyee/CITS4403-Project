import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
from empiricaldist import Pmf
from utils.utils import decorate


path = "../data"
rows = []

for filename in os.listdir(path):
	if filename.endswith(".graphml"):
		### real data
		realData = nx.read_graphml(os.path.join(path, filename))
		num_nodes = realData.number_of_nodes()
		num_edges = realData.number_of_edges()
		realDegrees = dict(realData.degree())
		realDegList = list(realDegrees.values())


		### BA Graph with same number of nodes as real data, and roughly the same degree as the real data (not exact)
		m = max(1, min(num_nodes - 1, int(round(num_edges / num_nodes))))
		baraAlbert = nx.barabasi_albert_graph(num_nodes, m)
		bADegrees = dict(baraAlbert.degree())
		bADegList = list(bADegrees.values())


		### create PMFs for these
		pmf_real = Pmf.from_seq(realDegList)
		pmf_ba = Pmf.from_seq(bADegList)


		plt.figure(figsize=(8, 6))
		options = dict(ls='', marker='.')

		plt.subplot(2, 2, 1)
		nx.draw(realData, node_size=20, node_color="skyblue", edge_color="gray", with_labels=False)
		plt.title(filename)

		plt.subplot(2, 2, 2)
		nx.draw(baraAlbert, node_size=20, node_color="lightcoral", edge_color="gray", with_labels=False)
		plt.title(f"BA {filename}")

		plt.subplot(2, 2, 3)
		pmf_real.plot(label=filename, color='C0', **options)
		decorate(xscale='log', yscale='log',xlim=[1, 1e4],xlabel='Degree',ylabel='PMF')
		plt.title(f"PMF {filename}")

		plt.subplot(2, 2, 4)
		pmf_ba.plot(label=f"BA {filename}", color='C1', **options)
		decorate(xscale='log',yscale='log',xlim=[1, 1e4],xlabel='Degree',ylabel='PMF')
		plt.title(f"PMF BA {filename}")

		plt.savefig(f"../figures/{filename}.png")
		plt.show()

		try:
			aspl_real = nx.average_shortest_path_length(realData)
			aspl_ba = nx.average_shortest_path_length(baraAlbert)
		except nx.NetworkXError:
			aspl_real = "Disconnected graph"
			aspl_ba = "Disconnected graph"

		rows.append({
			'Graph': filename,
			'Random_f_c': 'placeholder',
			'Targeted_f_c': 'placeholder',
			'Avg Shortest Path Length': aspl_real,
			'No. of Components': nx.number_connected_components(realData)
		})

		rows.append({
			'Graph': f" BA {filename}",
			'Random_f_c': 'placeholder',
			'Targeted_f_c': 'placeholder',
			'Avg Shortest Path Length': aspl_ba,
			'No. of Components': nx.number_connected_components(baraAlbert)
		})

df = pd.DataFrame(rows)
df.to_csv('../results/simulated_data.csv', index=False)
print(df)