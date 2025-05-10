import networkx as nx
import random


def to_multigraph(G: nx.Graph) -> nx.MultiGraph:
    """
    Convert a simple graph to a multigraph that allows for
    parallel edges.
    """

    MG = nx.MultiGraph()
    MG.add_nodes_from(G.nodes)
    MG.add_edges_from(G.edges)
    return MG


def get_connected_graph(num_nodes: int, num_edges: int = None) -> nx.Graph:
    """
    Generate a connected, undirected, unweighted simple graph.

    Parameters:
        num_nodes: Number of nodes (>= 2)
        num_edges: Optional number of edges (>= num_nodes - 1). If None, a random valid value is chosen.

    Returns:
        A connected NetworkX Graph.
        The graph contains no self-loops or parallel edges.
    """

    # Make sure there are enough nodes
    if num_nodes < 2:
        raise ValueError("Need at least 2 nodes for a meaningful graph.")

    # Make sure the number of edges are valid
    min_edges = num_nodes - 1
    max_edges = num_nodes * (num_nodes - 1) // 2

    if num_edges is None:
        num_edges = random.randint(min_edges, max_edges)
    elif num_edges < min_edges:
        raise ValueError("num_edges must be at least num_nodes - 1 to keep the graph connected.")
    elif num_edges > max_edges:
        raise ValueError("num_edges exceeds the maximum for a simple undirected graph.")

    # Start populating the graph
    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))

    # Step 1: Create a spanning tree to ensure connectivity
    # There will be exactly N - 1 edges after this step
    nodes = list(G.nodes)
    random.shuffle(nodes)
    for i in range(1, num_nodes):
        u = nodes[i]
        v = nodes[random.randint(0, i - 1)]
        G.add_edge(u, v)

    # Step 2: Add remaining unique edges
    remaining_edges = num_edges - min_edges
    existing_edges = set(G.edges())
    possible_edges = [(u, v) for u in range(num_nodes) for v in range(u + 1, num_nodes)
                      if (u, v) not in existing_edges]

    random.shuffle(possible_edges)
    G.add_edges_from(possible_edges[:remaining_edges])

    return G

