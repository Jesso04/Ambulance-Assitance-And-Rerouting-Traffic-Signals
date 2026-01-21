import random
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

from traffic_signals import update_signals, signal_states

# Load road network
graph = ox.load_graphml("city_graph.graphml")

# Generate a valid route
while True:
    start = random.choice(list(graph.nodes))
    end = random.choice(list(graph.nodes))
    try:
        route = nx.shortest_path(graph, start, end, weight="length")
        break
    except nx.NetworkXNoPath:
        continue

print("Route generated with", len(route), "nodes")

# Plot base map ONCE
fig, ax = ox.plot_graph(
    graph,
    node_size=0,
    edge_color="gray",
    show=False,
    close=False
)

# Lists to track plotted artists
signal_artists = []
ambulance_artist = None

# Live simulation
for i, node in enumerate(route):
    update_signals(route, i)

    # ✅ REMOVE previous signal dots
    for artist in signal_artists:
        artist.remove()
    signal_artists.clear()

    # ✅ REMOVE previous ambulance dot
    if ambulance_artist is not None:
        ambulance_artist.remove()

    # Plot traffic signals
    for signal_node, state in signal_states.items():
        y = graph.nodes[signal_node]["y"]
        x = graph.nodes[signal_node]["x"]

        if state == "GREEN":
            art = ax.scatter(x, y, c="green", s=30, zorder=3)
        else:
            art = ax.scatter(x, y, c="red", s=8, zorder=2)

        signal_artists.append(art)

    # Plot ambulance
    ay = graph.nodes[node]["y"]
    axx = graph.nodes[node]["x"]
    ambulance_artist = ax.scatter(axx, ay, c="blue", s=80, zorder=4)

    print(f"Ambulance at node {node}")
    plt.pause(1)

plt.show()
