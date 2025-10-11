import networkx as nx
import random
from src.constants import RANDOM_SEED

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