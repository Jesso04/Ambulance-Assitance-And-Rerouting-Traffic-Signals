import random
from pathlib import Path

import osmnx as ox
import networkx as nx

from backend.traffic_signals import update_signals, signal_states

# ---------------------------------------------------
# Load road network safely (path-independent)
# ---------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
GRAPH_PATH = BASE_DIR / "city_graph.graphml"

graph = ox.load_graphml(GRAPH_PATH)

# ---------------------------------------------------
# Generate a valid ambulance → hospital route
# ---------------------------------------------------
while True:
    start = random.choice(list(graph.nodes))
    end = random.choice(list(graph.nodes))
    try:
        route = nx.shortest_path(graph, start, end, weight="length")
        break
    except nx.NetworkXNoPath:
        continue

# ---------------------------------------------------
# Global state (ambulance position)
# ---------------------------------------------------
ambulance_index = 0


def step():
    """
    Move ambulance ONE step forward,
    update traffic signals (green corridor),
    and return clean, frontend-ready data.
    """
    global ambulance_index

    # Move ambulance forward
    if ambulance_index < len(route) - 1:
        ambulance_index += 1

    # Update traffic signals based on new position
    update_signals(route, ambulance_index)

    # Current ambulance node
    node = route[ambulance_index]
    amb_lat = graph.nodes[node]["y"]
    amb_lon = graph.nodes[node]["x"]

    # Collect GREEN signal coordinates (no raw IDs)
    green_signal_coords = []
    for signal_node, state in signal_states.items():
        if state == "GREEN":
            green_signal_coords.append({
                "lat": graph.nodes[signal_node]["y"],
                "lon": graph.nodes[signal_node]["x"]
            })

    # Return frontend-friendly JSON
    return {
        "ambulance": {
            "lat": amb_lat,
            "lon": amb_lon
        },
        "green_signals": green_signal_coords
    }
