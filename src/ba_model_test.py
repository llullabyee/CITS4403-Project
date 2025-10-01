import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os

from empiricaldist import Pmf
from utils.utils import decorate, savefig


path = "../data"


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

		plt.subplot(2, 2, 1)
		nx.draw(realData, node_size=20, node_color="skyblue", edge_color="gray", with_labels=False)
		plt.title(filename)

		plt.subplot(2, 2, 2)
		nx.draw(baraAlbert, node_size=20, node_color="lightcoral", edge_color="gray", with_labels=False)
		plt.title(f"BA {filename}")

		plt.subplot(2, 2, 3)
		pmf_real.plot(label=filename, color='C0')
		decorate(xlabel='Degree',ylabel='PMF')
		plt.title(f"PMF {filename}")

		plt.subplot(2, 2, 4)
		pmf_ba.plot(label=f"BA {filename}", color='C1')
		decorate(xlabel='Degree',ylabel='PMF')
		plt.title(f"PMF BA {filename}")

		plt.show()

