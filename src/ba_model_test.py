import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import os
from empiricaldist import Pmf
from utils.utils import decorate
from src.ba_functions import *
from utils.graph_visualization import color_critical_nodes
from src.heuristics import critical_fraction


path = os.path.join(os.path.dirname(__file__),'..' ,'data')
os.makedirs(os.path.join(os.path.dirname(__file__),'..' ,'figures'), exist_ok=True)
os.makedirs(os.path.join(os.path.dirname(__file__),'..' ,'results'), exist_ok=True)

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
		
        # Get critical fraction
		realCF = critical_fraction(realData)
		bACF = critical_fraction(baraAlbert)

		plt.figure(figsize=(19.2, 10.8))
		options = dict(ls='', marker='.')

		plt.subplot(2, 2, 1)
		realData_colorMap = color_critical_nodes(realData, realCF[1], "skyblue")
		nx.draw(realData, node_size=20, node_color=realData_colorMap, edge_color="gray", with_labels=False)
		plt.title(filename)

		plt.subplot(2, 2, 2)
		bA_colorMap = color_critical_nodes(baraAlbert, bACF[1], "lightcoral")
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

		plt.savefig(f"../figures/{filename}.png")
		plt.show()


		rows.append({
			'Graph': filename,
			'Random_f_c': 'placeholder',
			'Targeted_f_c': 'placeholder',
			'Avg Shortest Path Length': safeASPL(realData),
			'No. of Components': nx.number_connected_components(realData)
		})

		rows.append({
			'Graph': f" BA {filename}",
			'Random_f_c': 'placeholder',
			'Targeted_f_c': 'placeholder',
			'Avg Shortest Path Length': safeASPL(baraAlbert),
			'No. of Components': nx.number_connected_components(baraAlbert)
		})

df = pd.DataFrame(rows)
df.to_csv('../results/simulated_data.csv', index=False)
print(df)
