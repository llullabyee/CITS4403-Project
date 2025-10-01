import networkx as nx
import matplotlib.pyplot as plt
import os


path = "../data"


for filename in os.listdir(path):
	if filename.endswith(".graphml"):
		realData = nx.read_graphml(os.path.join(path, filename))
		num_nodes = realData.number_of_nodes()
		num_edges = realData.number_of_edges()
		m = max(1, min(num_nodes - 1, int(round(num_edges / num_nodes))))
		baraAlbert = nx.barabasi_albert_graph(num_nodes, m)
		plt.figure(figsize=(8, 6))

		plt.subplot(1, 2, 1)
		nx.draw(realData, node_size=20, node_color="skyblue", edge_color="gray", with_labels=False)
		plt.title(filename)

		plt.subplot(1, 2, 2)
		nx.draw(baraAlbert, node_size=20, node_color="lightcoral", edge_color="gray", with_labels=False)
		plt.title(f"BA {filename}")

		plt.show()

