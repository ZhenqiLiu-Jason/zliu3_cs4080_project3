import networkx as nx
import random


def karger_min_cut(original_graph: nx.Graph) -> int:
    # Work on a MultiGraph copy to preserve parallel edges during contraction
    G = nx.MultiGraph(original_graph)

    while G.number_of_nodes() > 2:
        # 1. Pick a random edge (u, v)
        u, v = random.choice(list(G.edges()))

        # 2. Contract node v into u
        for neighbor in list(G.neighbors(v)):
            # Add all edges from v to its neighbors (including u)
            G.add_edges_from([(u, neighbor)] * G.number_of_edges(v, neighbor))

        # 3. Remove the contracted node and self-loops
        G.remove_node(v)
        G.remove_edges_from(list(nx.selfloop_edges(G)))

    # Remaining edges between the 2 supernodes = cut size
    return G.number_of_edges()


def repeated_karger_min_cut(G: nx.Graph, trials: int = 100) -> int:
    min_cut = float('inf')
    for _ in range(trials):
        cut = karger_min_cut(G)
        min_cut = min(min_cut, cut)
    return min_cut
