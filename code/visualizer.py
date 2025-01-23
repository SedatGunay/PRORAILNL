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
    """Visualize k scores per iteration with a histogram with low bins."""
    plt.figure(figsize=(10, 6))
    
    plt.hist(k_scores, bins=100, color='blue', edgecolor='black', alpha=0.7)
    
    plt.xlabel('K-scores')
    plt.ylabel('Frequentie')
    plt.title('Histogram van K-scores')
    
    plt.show()

def scatterplot(trajectories):
    """ Plot the kscores and times of a trajectory in a scatterplot 
     - input parameter:  list of trajectories  """
    
    # Extract times and scores of trajectories
    total_times = [time for _, time, _ in trajectories]
    k_scores = [k_score for _, _, k_score in trajectories]

    # make the scatterplot
    plt.figure(figsize=(10, 6))
    plt.scatter(total_times, k_scores, color='dodgerblue', edgecolor='black',s=25)

    # add titels and labels
    plt.xlabel("Total Time (minutes)", fontsize=10)
    plt.ylabel("K-Score", fontsize=10)
    plt.title("K-Scores vs. Total Time of Trajectories", fontsize=12)

    # add grid
    plt.grid(True, linestyle='--', alpha=0.7)

    # show scatter
    plt.tight_layout()
    plt.show()




