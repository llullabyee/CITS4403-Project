import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from empiricaldist import Pmf
from utils.utils import decorate
from utils.graph_visualization import color_critical_nodes


def safeASPL(graph):
	if nx.number_connected_components(graph) > 1:
		gcc = max(nx.connected_components(graph), key=len)
		subgraph = graph.subgraph(gcc).copy()
		return nx.average_shortest_path_length(subgraph)
	else:
		return nx.average_shortest_path_length(graph)


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



