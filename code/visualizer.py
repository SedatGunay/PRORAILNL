import networkx as nx
import matplotlib.pyplot as plt
import random
import geopandas as gpd
from shapely.geometry import Point, LineString
import contextily as ctx

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

def visualize_network_on_map(rail_network, optimized_trajectories):
    # Zet stations om naar een GeoDataFrame en laat het traject op de map van NL zien
    station_geometries = [Point(station.x, station.y) for station in rail_network.stations.values()]
    station_names = [station.name for station in rail_network.stations.values()]
    stations_gdf = gpd.GeoDataFrame({"station": station_names}, geometry=station_geometries, crs="EPSG:4326")

    # Zet verbindingen om naar een GeoDataFrame
    connection_geometries = [
        LineString([(conn.station1.x, conn.station1.y), (conn.station2.x, conn.station2.y)])
        for conn in rail_network.connections
    ]
    connections_gdf = gpd.GeoDataFrame(geometry=connection_geometries, crs="EPSG:4326")

    # Zet trajecten om naar een GeoDataFrame
    trajectory_geometries = []
    for route, _ in optimized_trajectories:
        points = [(rail_network.stations[station].x, rail_network.stations[station].y) for station in route]
        trajectory_geometries.append(LineString(points))

    trajectories_gdf = gpd.GeoDataFrame(geometry=trajectory_geometries, crs="EPSG:4326")

    # Maak een plot
    fig, ax = plt.subplots(figsize=(12, 10))

    # Voeg de verbindingen toe
    connections_gdf.plot(ax=ax, color="grey", linewidth=0.5, alpha=0.7, label="Connections")

    # Voeg de stations toe
    stations_gdf.plot(ax=ax, color="blue", markersize=10, label="Stations")

    # Voeg trajecten toe met verschillende kleuren
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan', 'magenta', 'yellow']
    for idx, trajectory in enumerate(trajectories_gdf.geometry):
        trajectories_gdf.iloc[[idx]].plot(ax=ax, color=colors[idx % len(colors)], linewidth=2, label=f"Traject {idx + 1}")

    # Voeg een basemap toe
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, crs="EPSG:4326")

    # Pas layout aan
    ax.set_title("Rail Network and Trajectories on Map of the Netherlands", fontsize=14)
    ax.set_xlabel("Longitude", fontsize=12)
    ax.set_ylabel("Latitude", fontsize=12)
    ax.legend(loc="upper right")

    plt.show()

# visualizer.py
import matplotlib.pyplot as plt

def plot_k_scores(k_score_list):
    """
    Plot the progression of K-scores over iterations during an experiment
    
    Parameter:
        k_score_list (list): List of K-scores to plot.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(k_score_list)), k_score_list, label="K-Score over Iterations", color="blue")
    plt.title("K-Score Progression")
    plt.xlabel("Iteration")
    plt.ylabel("K-Score")
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_k_score_distribution(k_scores):
    """ 
    Plots the distribution of K-scores based on x runs of experiment
    Parameter:
    -k_scores (list) : A list of K-scores to plot
    """
    plt.hist(k_scores, bins = 20)
    plt.title("K-score Distribution")
    plt.xlabel("K-score")
    plt.ylabel("Frequency")
    plt.grid(True)

    plt.show()