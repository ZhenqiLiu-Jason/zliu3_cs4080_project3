import os
import networkx as nx
import numpy as np

from savefigure import save_plot
from get_graph import get_connected_graph, get_connected_multigraph, get_barbell_graph
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


def find_average_karger_accuracy(num_graphs: int, num_nodes: int, get_graph) -> float:
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
        G = get_graph(num_nodes)

        total_trials += find_karger_accuracy(G)
    return total_trials / num_graphs



# Start the main execution
# The experiment parameters
n_values = np.arange(4, 50)
num_graphs = 300


# Run the experiments
average_accuracy = np.array([find_average_karger_accuracy(num_graphs, n, get_connected_graph) for n in n_values])
average_barbell_accurace = np.array([find_average_karger_accuracy(num_graphs, n, get_barbell_graph) for n in n_values])

# Comparison plots
theory1 = 0.3 * n_values
theory2 = (n_values * (n_values - 1) / 2) * np.log(n_values)

# Create the directory, including any intermediate directories
os.makedirs('../images', exist_ok=True)

# Plot the results
save_plot(
    traces = {
        "Experimental(Random)": (n_values, average_accuracy, '-'),
        'Experimental(Barbell)': (n_values, average_barbell_accurace, '-'),
        r'$\frac{3n}{10}$': (n_values, theory1, '--')
    },
    filename='../images/karger_average_accuracy.png',
    xlabel=r'Number of Nodes (n)',
    ylabel=r'Average Trials to Find Min-Cut',
    title="Karger's Algorithm: Experimental vs. Theoretical",
    annotation=False)

save_plot(
    traces = {
        "Experimental(Random)": (n_values, average_accuracy, '-'),
        'Experimental(Barbell)': (n_values, average_barbell_accurace, '-'),
        r'$\frac{n(n - 1)}{2} \cdot \ln(n)$': (n_values, theory2, '-')
    },
    filename='../images/karger_average_accuracy_log_scale.png',
    xlabel=r'Number of Nodes (n)',
    ylabel=r'Average Trials to Find Min-Cut',
    title="Karger's Algorithm: Experimental vs. Theoretical",
    annotation=False,
    log_scale='y')
