import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import random

# Load previously saved graph
graph = ox.load_graphml("city_graph.graphml")

print("Graph loaded")
# Pick a random node as ambulance start
ambulance_node = random.choice(list(graph.nodes))

print("Ambulance start node:", ambulance_node)
# Pick a destination node far from start (hospital)
hospital_node = random.choice(list(graph.nodes))

print("Hospital node:", hospital_node)
# Compute shortest path based on distance
route = nx.shortest_path(
    graph,
    ambulance_node,
    hospital_node,
    weight="length"
)

print("Route length (nodes):", len(route))
# Plot route on map
fig, ax = ox.plot_graph_route(
    graph,
    route,
    route_linewidth=4,
    node_size=0,
    show=False,
    close=False
)
plt.show()


