import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

# 1️⃣ Choose a generic medium-size city
PLACE_NAME = "Indore, Madhya Pradesh, India"

# 2️⃣ Download road network (driveable roads only)
print("Downloading road network...")
graph = ox.graph_from_place(
    PLACE_NAME,
    network_type="drive"
)

# 3️⃣ Add distance (meters) to each road
graph = ox.add_edge_lengths(graph)

# 4️⃣ Save graph for reuse
ox.save_graphml(graph, "city_graph.graphml")

print("Graph loaded and saved successfully!")

# 5️⃣ Visualize (quick sanity check)
fig, ax = ox.plot_graph(
    graph,
    node_size=5,
    edge_linewidth=0.8,
    show=False,
    close=False
)
plt.show()
