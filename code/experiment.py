from classes.rail_network import RailNetwork
from greedy_selector import GreedyRouteSelector
from utils.helper import find_trajectories
from utils.scoring import calculate_K_score
from visualizer import visualize_network_on_map, plot_k_score_distribution
from depthclimber import DepthClimberRailNetwork
import csv
from random_baseline import Baseline

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

    """ --- Greedy Algorithm ---"""
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

    """--- Depth Climber ---"""
    depth_network = DepthClimberRailNetwork(max_time_limit=180)
    depth_network.load_stations(stations_file)
    depth_network.load_connections(connections_file)

    # Setup Depth Climber experiment
    full_k_scores = []
    real_highst_k = 0
    real_best_traject = None
    with open('depthclimberdata.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['K-Score', 'Trajectory'])
            
            for i in range(2, 21):
                initial_trajectories = depth_network.generate_initial_trajectories(num_trajectories=i)
                best_trajectory, best_K_score, k_score_list, trajectory_list = depth_network.hill_climber_depth_first(num_iterations=1, initial_trajectories=initial_trajectories)
            
                full_k_scores.extend(k_score_list)
                
                # Write each K-score and its corresponding trajectory to the CSV file
                for k_score, trajectory in zip(k_score_list, trajectory_list):
                    trajectory_str = ' -> '.join([str(station) for station in trajectory]) 
                    writer.writerow([k_score, trajectory_str])

                if best_K_score > real_highst_k:
                    real_highst_k = best_K_score
                    real_best_traject = best_trajectory

    print("Highest K-Score:", real_highst_k)
    print("Number of Routes used:", len(real_best_traject))
    plot_k_score_distribution(full_k_scores)

    """--- Random ---"""
    random_network = Baseline(180)
    random_network.load_stations("/Users/sedatgunay/Documents/GitHub/PRORAILNL/data/NL/StationsNationaal.csv")
    random_network.load_connections("/Users/sedatgunay/Documents/GitHub/PRORAILNL/data/NL/ConnectiesNationaal.csv")

    time_limit = 180 
    num_trajectories = 100000 

    # Generate and evaluate N random trajectories
    K_scores = random_network.calculate_kscore_trajectories(time_limit, num_trajectories)

    # Plot the distribution of K-scores
    plot_k_score_distribution(K_scores)

if __name__ == "__main__":
    main()

