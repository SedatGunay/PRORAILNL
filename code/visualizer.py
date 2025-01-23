import networkx as nx
import matplotlib.pyplot as plt
import random

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

    # Vooraf gedefinieerde kleuren voor de trajecten
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan', 'magenta', 'yellow']
    legend_labels = []

    # Teken de geoptimaliseerde trajecten met verschillende kleuren
    for idx, (route, duration) in enumerate(optimized_trajectories):
        color = colors[idx % len(colors)]  # Herhaal kleuren als er meer trajecten zijn dan kleuren
        nx.draw_networkx_edges(G, pos, edgelist=[(route[i], route[i + 1]) for i in range(len(route) - 1)],
                                 edge_color=color, width=2)
        legend_labels.append(f'Traject {idx + 1}')  # Voeg label toe voor de legenda

    # Voeg de legenda toe
    handles = [plt.Line2D([0], [0], color=colors[i % len(colors)], lw=2) for i in range(len(legend_labels))]
    plt.legend(handles, legend_labels, title="Trajecten", loc='upper left')

    plt.title("Rail Network Visualization")
    plt.show()