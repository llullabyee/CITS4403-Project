import matplotlib.pyplot as plt
import networkx as nx

from utils.utils import decorate

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

def plotter(subplot,graph,title,baseColor,nodelist=None, probMF=False):
	options = dict(ls='', marker='.')
	plt.subplot(subplot)
	if not probMF:
		colorMap = color_critical_nodes(graph, nodelist, baseColor)
		nx.draw(graph, node_size=20, node_color=colorMap, edge_color="gray", with_labels=False)
	else:
		graph.plot(label=title, color=baseColor, **options)
		decorate(xscale='log', yscale='log',xlim=[1, 1e4],xlabel='Degree',ylabel='PMF')
	plt.title(title)
