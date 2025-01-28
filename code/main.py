from classes.rail_network import RailNetwork
from algorithms.route_gen import find_trajectories, save_trajectories_to_file
from greedy_selector import GreedyRouteSelector
from visualizer import visualize_network, visualize_network_on_map, plot_k_score_distribution
from depthclimber import DepthClimberRailNetwork
from depth_first import DepthFirstRailNetwork
from hillclimbrandom import HillClimberRailNetwork
from utils.scoring import calculate_K_score

def run_greedy_test():
    print("Running Greedy Optimization...")

    stations_file = 'data/NL/StationsNationaal.csv'
    connections_file = 'data/NL/ConnectiesNationaal.csv'
    trajectories_output_file = 'data/trajectories_output.txt'
    
    rail_network = RailNetwork(180)
    rail_network.load_stations(stations_file)
    rail_network.load_connections(connections_file)

    max_duration = 180
    max_stations = 100
    max_reuse = 1
    trajectories = find_trajectories(rail_network, max_duration, max_stations, max_reuse)

    with open(trajectories_output_file, 'w') as output_file:
        for route, duration in trajectories:
            output_file.write(f"Path: {' -> '.join(route)}, Duration: {duration} minutes\n")
    
    print("Greedy Trajectories saved to:", trajectories_output_file)

    selector = GreedyRouteSelector(rail_network.connections)
    optimized_trajectories = selector.greedy_optimization(trajectories)
    k_score = calculate_K_score(optimized_trajectories, rail_network.connections)
    
    print("Greedy Optimized Trajectories:")
    for i, (route, duration) in enumerate(optimized_trajectories, 1):
        print(f"Path {i}: {' -> '.join(route)}, Duration: {duration} minutes")
    print(f"Greedy Final K-Score: {k_score}")

    visualize_network_on_map(rail_network, optimized_trajectories)

def run_depth_climber_test():
    print("Running Depth Climber Optimization...")
 
    rail_network = DepthClimberRailNetwork(max_time_limit=180)
    rail_network.load_stations('data/NL/StationsNationaal.csv')
    rail_network.load_connections('data/NL/ConnectiesNationaal.csv')

    full_k_scores = []
    real_highst_k = 0
    real_best_traject = None

    for i in range(2, 21):
        initial_trajectories = rail_network.generate_initial_trajectories(num_trajectories=i)
        best_trajectory, best_K_score, k_score_list = rail_network.hill_climber_depth_first(num_iterations=1000, initial_trajectories=initial_trajectories)
        if best_K_score > real_highst_k:
            real_highst_k = best_K_score
            real_best_traject = best_trajectory

        full_k_scores += k_score_list

    print("Highest K-Score:", real_highst_k)
    print("Number of Routes used:", len(real_best_traject))

    plot_k_score_distribution(full_k_scores)


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
    
    plot_k_score_distribution(full_k_scores)

def main():
    # Run each test function
    run_greedy_test()
    run_depth_climber_test()
    run_hill_climber_test()

if __name__ == "__main__":
    main()
