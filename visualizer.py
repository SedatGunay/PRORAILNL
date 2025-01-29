import networkx as nx
import matplotlib.pyplot as plt
import random
import geopandas as gpd
from shapely.geometry import Point, LineString
import contextily as ctx
import pandas as pd
import numpy as np

def visualize_network(rail_network, optimized_trajectories):
    """
    Visualizes the railway network using NetworkX and Matplotlib.
    """
    G = nx.Graph()

    # Add stations (nodes) to the graph
    for station in rail_network.stations.values():
        G.add_node(station.name, pos=(station.x, station.y))

    # Add connections (edges) to the graph
    for connection in rail_network.connections:
        G.add_edge(connection.station1.name, connection.station2.name)

    # Retrieve positions for visualization
    pos = nx.get_node_attributes(G, 'pos')

    # Draw the network
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_size=300, node_color='lightblue', edge_color='grey', font_size=8)

    # Predefined colors for different trajectories
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan', 'magenta', 'yellow']
    legend_labels = []

    # Draw the optimized trajectories with different colors
    for idx, (route, duration) in enumerate(optimized_trajectories):
        color = colors[idx % len(colors)]  # Cycle through colors if more trajectories exist
        nx.draw_networkx_edges(G, pos, edgelist=[(route[i], route[i + 1]) for i in range(len(route) - 1)],
                               edge_color=color, width=2)
        legend_labels.append(f'Trajectory {idx + 1}')  # Add legend label

    # Add legend
    handles = [plt.Line2D([0], [0], color=colors[i % len(colors)], lw=2) for i in range(len(legend_labels))]
    plt.legend(handles, legend_labels, title="Trajectories", loc='upper left')

    plt.title("Railway Network Visualization")
    plt.show()


def visualize_network_on_map(rail_network, optimized_trajectories):
    """
    Visualizes the railway network on a geographical map using GeoPandas.
    """
    # Convert stations to a GeoDataFrame
    station_geometries = [Point(station.x, station.y) for station in rail_network.stations.values()]
    station_names = [station.name for station in rail_network.stations.values()]
    stations_gdf = gpd.GeoDataFrame({"station": station_names}, geometry=station_geometries, crs="EPSG:4326")

    # Convert connections to a GeoDataFrame
    connection_geometries = [
        LineString([(conn.station1.x, conn.station1.y), (conn.station2.x, conn.station2.y)])
        for conn in rail_network.connections
    ]
    connections_gdf = gpd.GeoDataFrame(geometry=connection_geometries, crs="EPSG:4326")

    # Convert trajectories to a GeoDataFrame
    trajectory_geometries = []
    for route, _ in optimized_trajectories:
        points = [(rail_network.stations[station].x, rail_network.stations[station].y) for station in route]
        trajectory_geometries.append(LineString(points))

    trajectories_gdf = gpd.GeoDataFrame(geometry=trajectory_geometries, crs="EPSG:4326")

    # Create a plot
    fig, ax = plt.subplots(figsize=(12, 10))

    # Plot connections
    connections_gdf.plot(ax=ax, color="grey", linewidth=0.5, alpha=0.7, label="Connections")

    # Plot stations
    stations_gdf.plot(ax=ax, color="blue", markersize=10, label="Stations")

    # Plot trajectories with different colors
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan', 'magenta', 'yellow']
    for idx, trajectory in enumerate(trajectories_gdf.geometry):
        trajectories_gdf.iloc[[idx]].plot(ax=ax, color=colors[idx % len(colors)], linewidth=2, label=f"Trajectory {idx + 1}")

    # Add a basemap
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, crs="EPSG:4326")

    # Adjust layout
    ax.set_title("Railway Network and Trajectories on the Map", fontsize=14)
    ax.set_xlabel("Longitude", fontsize=12)
    ax.set_ylabel("Latitude", fontsize=12)
    ax.legend(loc="upper right")

    plt.show()


def plot_k_scores(k_score_list):
    """
    Plots the progression of K-scores over iterations during an experiment.
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
    Plots the distribution of K-scores from multiple experiment runs.
    """
    plt.hist(k_scores, bins=20, edgecolor='black', alpha=0.75)
    plt.title("K-Score Distribution")
    plt.xlabel("K-Score")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()


def plot_scores_from_csv(csv_file_path):
    """
    Reads K-scores from a CSV file and plots the distribution.

    Parameters:
    -----------
    csv_file_path : str
        Path to the CSV file containing the 'K-Score' column.
    """
    try:
        # Load the CSV file
        data = pd.read_csv(csv_file_path)

        # Ensure 'K-Score' column exists
        if 'K-Score' not in data.columns:
            print(f"Error: 'K-Score' column not found in {csv_file_path}.")
            return

        # Extract K-scores
        k_scores = data['K-Score']

        # Plot the distribution
        plt.figure(figsize=(10, 6))
        plt.hist(k_scores, bins=20, edgecolor='black', alpha=0.75)
        plt.title("K-Score Distribution")
        plt.xlabel("K-Score")
        plt.ylabel("Frequency")
        plt.grid(True)
        plt.show()

    except Exception as e:
        print(f"Error while plotting scores from {csv_file_path}: {e}")

def plot_duration_vs_score(k_score_list, trajectory_list):
    """
    Creates a scatterplot showing the relationship between total duration of trajectories 
    and their corresponding K-scores.
    """
    # Calculate total duration for each set of trajectories
    total_durations = [sum(len(route) for route in trajectories) if isinstance(trajectories, list) else 0 for trajectories in trajectory_list]

    
    plt.figure(figsize=(10, 6))
    plt.scatter(total_durations, k_score_list, alpha=0.6, c='blue', edgecolors='w', s=100)
    plt.title("Total Duration vs K-Score")
    plt.xlabel("Total Duration (in minutes)")
    plt.ylabel("K-Score")
    plt.grid(True)
    plt.show()

