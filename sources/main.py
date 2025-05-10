import networkx as nx
from get_graph import *


G = get_connected_graph(5)

print("Edges:", list(G.edges))
print("Is connected?", nx.is_connected(G))
print("Number of edges:", G.number_of_edges())

cut_value, partition = nx.stoer_wagner(G)
print(cut_value)
