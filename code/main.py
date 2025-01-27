from classes.rail_network import RailNetwork
from algorithms.route_gen import find_trajectories, save_trajectories_to_file
from algorithms.greedy_selector import GreedyRouteSelector
from visualizer import visualize_network, visualize_network_on_map
from depthclimber import DepthClimberRailNetwork
from depth_first import DepthFirstRailNetwork
from hillclimbrandom import HillClimberRailNetwork

def main():
    # Load data
    stations_file = 'data/NL/StationsNationaal.csv'
    connections_file = 'data/NL/ConnectiesNationaal.csv'
    trajectories_output_file = 'data/trajectories_output.txt'
    
    # Initialize RailNetwork and load data
    rail_network = RailNetwork(180)
    rail_network.load_stations(stations_file)
    rail_network.load_connections(connections_file)

    # Generate trajectories
    max_duration = 180
    max_stations = 100
    max_reuse = 1
    trajectories = find_trajectories(rail_network, max_duration, max_stations, max_reuse)

    # Save trajectories to file
    with open(trajectories_output_file, 'w') as output_file:
        for route, duration in trajectories:
            output_file.write(f"Path: {' -> '.join(route)}, Duration: {duration} minutes\n")
    
    print("Trajectories saved to:", trajectories_output_file)

    # Optimize trajectories using GreedyRouteSelector
    selector = GreedyRouteSelector(rail_network.connections)
    optimized_trajectories = selector.greedy_optimization(trajectories)
    k_score = selector.calculate_K_score(optimized_trajectories)
    
    i = 1
    print("Optimized Trajectories:")
    for route, duration in optimized_trajectories:
        print(f"Path {i}: {' -> '.join(route)}, Duration: {duration} minutes")
        i += 1
    print(f"Final K-Score: {k_score}")

    # Visualize
    visualize_network_on_map(rail_network, optimized_trajectories)

if __name__ == "__main__":
    main()

