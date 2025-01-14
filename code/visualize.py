import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np

def visualize_network(rail_network, trajectories):
    """ Makes a graph of the connections of the trajectories to show the network"""
    # make empty graph
    G = nx.Graph()
    
    # Add stations as nodes 
    for station_name, station in rail_network.stations.items():
        G.add_node(station_name, pos=(station.x, station.y))
    
    # Add connections as edges
    for connection in rail_network.connections:
        G.add_edge(connection.station1, connection.station2, weight=connection.distance)
    
    # Positions of stations
    pos = nx.get_node_attributes(G, 'pos')
    
    # Plot graph
    plt.figure(figsize=(10, 8))
    
    # Draw connections in grey
    nx.draw(G, pos, with_labels=True, node_size=300, node_color='lightblue', edge_color='grey', font_size=8)
    
    # Draw trajectories with different colors 
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan', 'brown']
    for i, (trajectory, _) in enumerate(trajectories):
        color = colors[i % len(colors)]  # Reuse colors if len trajectories is longer than colors
        edges = [(trajectory[j], trajectory[j+1]) for j in range(len(trajectory) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=color, width=2)
    
    plt.title("Rail Network Trajectories")
    plt.show()

def visualize_k_scores(k_scores):
    """Visualiseer de K-scores per iteratie in een histogram."""
    plt.figure(figsize=(10, 6))
    

    plt.plot(range(1, len(k_scores) + 1), k_scores, linestyle='-', color='b')
    
    plt.xlabel('Iteraties')
    plt.ylabel('K-score')
    plt.title('K-scores per Iteratie')
    
    plt.show()
