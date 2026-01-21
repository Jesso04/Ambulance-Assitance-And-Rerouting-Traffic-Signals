import osmnx as ox
from pathlib import Path

# Get backend directory path
BASE_DIR = Path(__file__).resolve().parent

# Load road graph safely
graph = ox.load_graphml(BASE_DIR / "city_graph.graphml")

# Nodes with degree >= 3 are treated as traffic signals
traffic_signals = {
    node for node, degree in graph.degree() if degree >= 3
}

# Initialize signal states
signal_states = {node: "RED" for node in traffic_signals}

GREEN_WINDOW = 8


def update_signals(route, ambulance_index):
    """
    Update traffic signals based on ambulance position
    """
    for node in signal_states:
        signal_states[node] = "RED"

    upcoming_nodes = route[ambulance_index : ambulance_index + GREEN_WINDOW]
    for node in upcoming_nodes:
        if node in signal_states:
            signal_states[node] = "GREEN"
