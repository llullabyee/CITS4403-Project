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