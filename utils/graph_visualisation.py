import matplotlib.pyplot as plt
import networkx as nx
import os

from utils.utils import decorate
from src.constants import FIGURES_VISUAL_PATH
from empiricaldist import Cdf
"""
	Utility functions for graph visualization
"""


def color_critical_nodes (graph, nodes, base_color, highlight_color='red'):
	"""
	Get color map for critical nodes.
	@param: graph which is a networkx graph
	@param: nodes which is a list of nodes in the graph
	@param: the base color for the nodes
	@param: the optional highlight color
	@returns and list of colors that correspond to the nodes in the graph.
	"""
	# https://stackoverflow.com/a/33131451
	color_map = []
	for node in graph:
		if node in nodes:
			color_map.append(highlight_color)
		else:
			color_map.append(base_color)
	return color_map

def model_plotter(subplot,graph,title,baseColor,nodelist=None, probMF=False):
	options = dict(ls='', marker='.')
	plt.subplot(subplot)
	if not probMF:
		colorMap = color_critical_nodes(graph, nodelist, baseColor)
		nx.draw(graph, node_size=20, node_color=colorMap, edge_color="gray", with_labels=False)
	else:
		graph.plot(label=title, color=baseColor, **options)
		decorate(xscale='log', yscale='log',xlim=[1, 1e4],xlabel='Degree',ylabel='PMF')
	plt.title(title)

def cdf_plotter(real, ba, hk, title, x, y):
	plt.figure(figsize=(19.2, 10.8))
	for seq, label, color in zip([real, ba, hk],
				     ["Real", "BA", "HK"],
				     ["blue", "purple", "green"]):
		cdf = Cdf.from_seq(seq)
		plt.plot(cdf.index, cdf.values, label=label, color=color)
		plt.fill_between(cdf.index, 0, cdf.values, color=color, alpha=0.2)
	plt.title(title)
	plt.ylabel(y)
	plt.xlabel(x)
	plt.legend()
	plt.savefig(f"{os.path.join(FIGURES_VISUAL_PATH, title)}.png")
	plt.close()

def hist_plotter(real, ba, hk, title, x, y):
	plt.figure(figsize=(19.2, 10.8))
	plt.hist([real, ba, hk], bins=20, density=True,
		 color=["blue", "purple", "green"], alpha=0.5, label=["Real", "BA", "HK"])
	plt.title(title)
	plt.ylabel(y)
	plt.xlabel(x)
	plt.legend()
	plt.savefig(f"{os.path.join(FIGURES_VISUAL_PATH, title)}.png")
	plt.close()