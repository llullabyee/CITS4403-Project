import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from empiricaldist import Pmf
from utils.utils import decorate


def safeASPL(graph):
	if nx.number_connected_components(graph) > 1:
		gcc = max(nx.connected_components(graph), key=len)
		subgraph = graph.subgraph(gcc).copy()
		return nx.average_shortest_path_length(subgraph)
	else:
		return nx.average_shortest_path_length(graph)
