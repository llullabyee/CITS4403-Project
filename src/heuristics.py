import networkx as nx
import random
import os

from src.constants import RANDOM_SEED, DATASET_PATH
from empiricaldist import Pmf


def critical_fraction (graph: nx.Graph, randomFailure=True, threshold=0.5) -> tuple:
	"""
	Returns the critical fraction of nodes (the smallest number) that can be removed before,
	The largest connected component in the graph is proportionally lesser to the original graph by the threshold.
	@param: a networkx graph object
	@param: random: whether the code performs a randomised node failure or targeted node attack.
	@param: an optional threshold for the critical fraction threshold
	@return: A tuple of the (fraction of nodes, list of removed nodes) or None (which should not be possible)
	"""
	# 1. Get the nodes in the graph
	nodes = list (graph.nodes)
	total_nodes = len (nodes)

	# 2. Order nodes in terms of degree - this ensures that the smallest number of nodes are selected
	# https://stackoverflow.com/a/48382895
	if randomFailure is True:
		nodes_by_degree = list(graph.degree())
		# set the random seed
		random.seed (RANDOM_SEED)
		random.shuffle(nodes_by_degree)
	else:
		nodes_by_degree = sorted(graph.degree, key=lambda x: x[1], reverse=True)

	# 3. Track the removed nodes, and copy the original graph to remove nodes from it
	removed_nodes = []
	graph_remove = graph.copy()

	# 4. Remove each node
	for node_entry in nodes_by_degree:
		node = node_entry[0]
		graph_remove.remove_node(node)
		removed_nodes.append(node)

		# 5. Calculate the critical fraction and return
		if len(graph_remove) > 0:
			# get size of GCC : https://stackoverflow.com/a/62838497
			GCCs = sorted(nx.connected_components(graph_remove), key=len, reverse=True)
			giantCC = graph_remove.subgraph(GCCs[0])
			CF = len (giantCC) / total_nodes
			if (CF < threshold):
				node_frac = len (removed_nodes) / total_nodes
				return (node_frac, removed_nodes)
		else:
			return (1.0, removed_nodes) # 1 indicates full disconnection


def safeASPL(graph):
	if nx.number_connected_components(graph) > 1:
		gcc = max(nx.connected_components(graph), key=len)
		subgraph = graph.subgraph(gcc).copy()
		return nx.average_shortest_path_length(subgraph)
	else:
		return nx.average_shortest_path_length(graph)


def gccSimulation(realData):
	### real data
	num_nodes = realData.number_of_nodes()
	num_edges = realData.number_of_edges()
	realDegrees = dict(realData.degree())
	realDegList = list(realDegrees.values())
	realACC = nx.average_clustering(nx.Graph(realData))

	m = max(1, min(num_nodes - 1, int(round(num_edges / num_nodes))))

	### BA Graph with same number of nodes as real data, and roughly the same degree as the real data (not exact)
	baraAlbert = nx.barabasi_albert_graph(num_nodes, m, seed=RANDOM_SEED)
	bADegrees = dict(baraAlbert.degree())
	bADegList = list(bADegrees.values())
	bAACC = nx.average_clustering(nx.Graph(baraAlbert))

	### HK Graph, Same Parameters as BA
	holmesKim = nx.powerlaw_cluster_graph(num_nodes, m, realACC, seed=RANDOM_SEED)
	hKDegrees = dict(holmesKim.degree())
	hKDegList = list(hKDegrees.values())
	hkACC = nx.average_clustering(nx.Graph(holmesKim))

	### create PMFs for these
	pmf_real = Pmf.from_seq(realDegList)
	pmf_ba = Pmf.from_seq(bADegList)
	pmf_hk = Pmf.from_seq(hKDegList)

	return baraAlbert, holmesKim, pmf_real, pmf_ba, pmf_hk, realACC, bAACC, hkACC


def get_crit_frac(real,ba,hk):
	realRCF, realRandNodeRemoved = critical_fraction(real)
	realTCF, realTargetNodeRemoved = critical_fraction(real, False)
	bARCF, bARandNodeRemoved = critical_fraction(ba)
	bATCF, bATargetNodeRemoved = critical_fraction(ba, False)
	hkRCF, hkRandNodeRemoved = critical_fraction(hk)
	hkTCF, hkTargetNodeRemoved = critical_fraction(hk, False)
	return (realRCF, realRandNodeRemoved, realTCF, realTargetNodeRemoved, bARCF,
		bARandNodeRemoved, bATCF, bATargetNodeRemoved, hkRCF, hkRandNodeRemoved,
		hkTCF, hkTargetNodeRemoved)
