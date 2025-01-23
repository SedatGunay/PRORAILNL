import networkx as nx
import matplotlib.pyplot as plt

def visualize_network(rail_network, optimized_trajectories):
    G = nx.Graph()

    # Voeg knopen toe aan de grafiek
    for station in rail_network.stations.values():
        G.add_node(station.name, pos=(station.x, station.y))  # Gebruik de x en y coördinaten van de station

    # Voeg verbindingen toe aan de grafiek
    for connection in rail_network.connections:
        G.add_edge(connection.station1.name, connection.station2.name)

    # Haal de posities op
    pos = nx.get_node_attributes(G, 'pos')

    # Teken het netwerk
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_size=300, node_color='lightblue', edge_color='grey', font_size=8)

    # Teken de geoptimaliseerde trajecten
    for route, duration in optimized_trajectories:
        nx.draw_networkx_edges(G, pos, edgelist=[(route[i], route[i + 1]) for i in range(len(route) - 1)], edge_color='red', width=2)

    plt.title("Rail Network Visualization")
    plt.show()
