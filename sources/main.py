import networkx as nx

from get_graph import *
from karger_algo import *


G = get_connected_graph(100)

print("Edges:", list(G.edges))
print("Is connected?", nx.is_connected(G))
print("Number of edges:", G.number_of_edges())

cut_value, partition = nx.stoer_wagner(G)
print(cut_value)

print("Estimated min-cut:", repeated_karger_min_cut(G, trials=15))
