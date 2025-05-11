import networkx as nx

from savefigure import save_plot
from get_graph import get_connected_graph, get_connected_multigraph
from karger_algo import karger_min_cut, repeated_karger_min_cut


def find_karger_accuracy(G: nx.Graph) -> int:
    """
    Find out how many times needed to run karger before it finds
    the right min-cut value.
    """

    # Get the true min-cut value
    true_min_cut, _ = nx.stoer_wagner(G)

    # Find how many trials are needed
    trials = 1
    while karger_min_cut(G) != true_min_cut:
        trials += 1

    return trials


def find_average_karger_accuracy(num_graphs: int, num_nodes: int) -> float:
    """
    Find the average amount of trials needed to run karger before it
    find the right min-cut value for graphs with the specified amount
    of nodes. The more random graphs are used, the better the average
    will be.

    Answers this question:
    On average, how many trials of Karger's algorithm are 
    needed to find the true min-cut on a random graph of size n?
    """

    total_trials = 0
    for _ in range(num_graphs):

        # Generate a random graph each time to avoid bias
        G = get_connected_graph(num_nodes)

        total_trials += find_karger_accuracy(G)
    return total_trials / num_graphs

