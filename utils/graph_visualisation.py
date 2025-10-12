import matplotlib.pyplot as plt
import networkx as nx
import os
import numpy as np
import pandas as pd
import seaborn as sns

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


def plot_models(configs, save_path, dataTitle):
	plt.figure(figsize=(19.2, 10.8))
	for i, (graph, label, color, target_nodes, pmf_data, probMF) in enumerate(configs, start=231):
		model_plotter(i, graph, f"{label} {dataTitle}", color, target_nodes)
		model_plotter(i+3, pmf_data, f"PMF {label} {dataTitle}", color, probMF=probMF)
	plt.savefig(save_path)
	plt.close()

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


def visualize_network_metrics(real, ba, hk, suffix=""):
	"""Plot CDF, histogram, and heatmap for the given datasets."""
	# Unpack CSV data
	realRCF, realTCF, realASPL, realACC, realCCs = real
	bARCF, bATCF, bAASPL, bAACC, bACCs = ba
	hkRCF, hkTCF, hkASPL, hkACC, hkCCs = hk

	# Define metrics for iteration
	metrics = [
		("RCF", realRCF, bARCF, hkRCF, "Critical Fraction"),
		("TCF", realTCF, bATCF, hkTCF, "Critical Fraction"),
		("ASPL", realASPL, bAASPL, hkASPL, "Average Shortest Path Length"),
		("ACC", realACC, bAACC, hkACC, "Average Clustering Coefficient")
	]

	# Plot CDF and histograms
	for name, real_data, ba_data, hk_data, xlabel in metrics:
		cdf_plotter(real_data, ba_data, hk_data,
			    f"CDF - {name}{suffix}", xlabel, "Cumulative Probability")
		hist_plotter(real_data, ba_data, hk_data,
			     f"Histogram - {name}{suffix}", xlabel, "Probability Density")

	# Heatmap
	data = pd.DataFrame({
		"Network": ["Real", "BA", "HK"],
		"RCF": [np.mean(realRCF), np.mean(bARCF), np.mean(hkRCF)],
		"TCF": [np.mean(realTCF), np.mean(bATCF), np.mean(hkTCF)],
		"ASPL": [np.mean(realASPL), np.mean(bAASPL), np.mean(hkASPL)],
		"ACC": [np.mean(realACC), np.mean(bAACC), np.mean(hkACC)],
		"CCs": [np.mean(realCCs), np.mean(bACCs), np.mean(hkCCs)]
	})
	data.set_index("Network", inplace=True)

	plt.figure(figsize=(9,5))
	sns.heatmap(data, annot=True, cmap="coolwarm", fmt=".2f")
	plt.title(f"Network Metrics Comparison{suffix}")
	plt.savefig(os.path.join(FIGURES_VISUAL_PATH, f"Network Metrics Comparison{suffix}.png"))
	plt.close()