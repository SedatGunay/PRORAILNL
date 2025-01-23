import networkx as nx
import matplotlib.pyplot as plt

def visualize_network(rail_network, trajectories):
    G = nx.Graph()
    for station_name, station in rail_network.stations.items():
        G.add_node(station_name, pos=(station.x, station.y))
    for connection in rail_network.connections:
        G.add_edge(connection.station1.name, connection.station2.name, weight=connection.distance)
    pos = nx.get_node_attributes(G, 'pos')
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_size=300, node_color='lightblue', edge_color='grey', font_size=8)
    colors = ['red', 'blue', 'green', 'orange', 'purple']
    for i, (trajectory, _) in enumerate(trajectories):
        edges = [(trajectory[j], trajectory[j + 1]) for j in range(len(trajectory) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=colors[i % len(colors)], width=2)
    plt.title("Rail Network Trajectories")
    plt.show()
