from classes.rail_network import RailNetwork
from algorithms.route_gen import find_trajectories, save_trajectories_to_file
from greedy_selector import GreedyRouteSelector
from visualizer import visualize_network, visualize_network_on_map
from depthclimber import DepthClimberRailNetwork
from depth_first import DepthFirstRailNetwork
from hillclimbrandom import HillClimberRailNetwork

def run_greedy_test():
    print("Running Greedy Optimization...")
    # Load data
    stations_file = 'data/NL/StationsNationaal.csv'
    connections_file = 'data/NL/ConnectiesNationaal.csv'
    trajectories_output_file = 'data/trajectories_output.txt'
    
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
    
    print("Greedy Trajectories saved to:", trajectories_output_file)

    # Optimize trajectories using GreedyRouteSelector
    selector = GreedyRouteSelector(rail_network.connections)
    optimized_trajectories = selector.greedy_optimization(trajectories)
    k_score = selector.calculate_K_score(optimized_trajectories)
    
    print("Greedy Optimized Trajectories:")
    for i, (route, duration) in enumerate(optimized_trajectories, 1):
        print(f"Path {i}: {' -> '.join(route)}, Duration: {duration} minutes")
    print(f"Greedy Final K-Score: {k_score}")

    # Visualize
    visualize_network_on_map(rail_network, optimized_trajectories)

def run_depth_climber_test():
    print("Running Depth Climber Optimization...")
    rail_network = DepthClimberRailNetwork(max_time_limit=180)
    rail_network.load_stations('data/NL/StationsNationaal.csv')
    rail_network.load_connections('data/NL/ConnectiesNationaal.csv')

    full_k_scores = []
    highest_k_score_overall = 0
    best_trajectories_overall = None

    for num_routes in range(2, 21):
        print(f"Running Depth Climber with {num_routes} routes...")

        best_trajectories, highest_k_score, k_score_list = rail_network.hill_climber_optimization(num_iterations=10000, num_routes=num_routes)

        if highest_k_score > highest_k_score_overall:
            highest_k_score_overall = highest_k_score
            best_trajectories_overall = best_trajectories

        full_k_scores += k_score_list

    print("Depth Climber Highest K-Score:", highest_k_score_overall)
    print("Number of Routes used:", len(best_trajectories_overall))
    
    visualize_network_on_map(rail_network, best_trajectories_overall)

def run_hill_climber_test():
    print("Running Hill Climber Optimization...")
    rail_network = HillClimberRailNetwork(max_time_limit=180)
    rail_network.load_stations('data/NL/StationsNationaal.csv')
    rail_network.load_connections('data/NL/ConnectiesNationaal.csv')

    full_k_scores = []
    highest_k_score_overall = 0
    best_trajectories_overall = None

    for num_routes in range(2, 21):
        print(f"Running Hill Climber with {num_routes} routes...")

        best_trajectories, highest_k_score, k_score_list = rail_network.hill_climber_optimization(num_iterations=10000, num_routes=num_routes)

        if highest_k_score > highest_k_score_overall:
            highest_k_score_overall = highest_k_score
            best_trajectories_overall = best_trajectories

        full_k_scores += k_score_list

    print("Hill Climber Highest K-Score:", highest_k_score_overall)
    print("Number of Routes used:", len(best_trajectories_overall))
    
    visualize_network_on_map(rail_network, best_trajectories_overall)

def main():
    # Run each test function
    run_greedy_test()
    run_depth_climber_test()
    run_hill_climber_test()

if __name__ == "__main__":
    main()
