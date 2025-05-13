import networkx as nx
import random


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


def get_connected_multigraph(num_nodes: int, num_edges: int = None) -> nx.MultiGraph:
    """
    Randomly generate a connected, undirected and unweighted multigraph.
    """

    if num_nodes < 2:
        raise ValueError("Need at least 2 nodes for a meaningful graph.")

    G = nx.MultiGraph()
    G.add_nodes_from(range(num_nodes))

    # Step 1: Create a spanning tree to ensure connectivity
    nodes = list(G.nodes)
    random.shuffle(nodes)
    for i in range(1, num_nodes):
        u = nodes[i]
        v = nodes[random.randint(0, i - 1)]
        G.add_edge(u, v)

    # Making sure the number of edges is valid
    min_edges = num_nodes - 1
    if num_edges is None:
        num_edges = min_edges + random.randint(1, num_nodes)  # slightly more edges
    elif num_edges < min_edges:
        raise ValueError("num_edges must be at least num_nodes - 1 to keep the graph connected.")

    # Step 2: Add remaining random edges (allowing parallel edges)
    remaining_edges = num_edges - min_edges
    while remaining_edges > 0:
        u, v = random.sample(range(num_nodes), 2)
        G.add_edge(u, v)
        remaining_edges -= 1

    return G


def get_barbell_graph(num_nodes: int, bridge_edges: int = 1) -> nx.Graph:
    """
    Generates a barbell-like graph:
    - Two cliques of equal size
    - A few edges connecting them (forming the bridge)

    Parameters:
        num_nodes: total number of nodes
        bridge_edges: number of edges connecting the two cliques

    Returns:
        A connected NetworkX Graph with a narrow min-cut
    """

    if num_nodes < 4:
        raise ValueError("num_nodes should be at least 4 for a barbell graph.")

    half = num_nodes // 2
    G = nx.Graph()

    # Add first clique
    left = range(half)
    G.add_nodes_from(left)
    for i in left:
        for j in left:
            if i < j:
                G.add_edge(i, j)

    # Add second clique
    right = range(half, num_nodes)
    G.add_nodes_from(right)
    for i in right:
        for j in right:
            if i < j:
                G.add_edge(i, j)

    # Add bridge edges (randomly connect left to right)
    bridge_pairs = random.sample([(u, v) for u in left for v in right], bridge_edges)
    G.add_edges_from(bridge_pairs)

    return G
