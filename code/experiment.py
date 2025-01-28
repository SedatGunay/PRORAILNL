from classes.rail_network import RailNetwork
from greedy_selector import GreedyRouteSelector
from utils.helper import find_trajectories
from utils.scoring import calculate_K_score
from visualizer import visualize_network_on_map

def main():
    # Load data
    stations_file = 'data/NL/StationsNationaal.csv'
    connections_file = 'data/NL/ConnectiesNationaal.csv'

    # Initialize RailNetwork and load data
    rail_network = RailNetwork(180)
    rail_network.load_stations(stations_file)
    rail_network.load_connections(connections_file)
    
    # Generate possible trajectories 
    max_duration = 180
    max_stations = 100
    max_reuse = 1
    trajectories = find_trajectories(rail_network, max_duration, max_stations, max_reuse)

    """ ---Greedy Algorithm---"""
    greedy = GreedyRouteSelector(rail_network.connections)
    optimized_trajectory_greedy = greedy.greedy_optimization(trajectories)

    # Calculate k score 
    k_score_greedy = calculate_K_score(optimized_trajectory_greedy, rail_network.connections)
    print(f"The K-score for Greedy optimazation is: {k_score_greedy}")

    # Print optimized trajectories 
    print("The optimized trajectories are:")
    i = 1 
    for route, duration in optimized_trajectory_greedy:
        print(f"Trajectory {i}: {' -> '.join(route)}, Duration: {duration} minutes")
        print()
        i += 1
    
    # Visualize the final greedy network 
    visualize_network_on_map(rail_network, optimized_trajectory_greedy)


if __name__ == "__main__":
    main()

