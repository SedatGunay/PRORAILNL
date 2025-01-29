from classes.rail_network import RailNetwork
from algorithms.greedy_selector import GreedyRouteSelector
from utils.helper import find_trajectories
from utils.scoring import calculate_K_score
from visualizer import visualize_network_on_map, plot_k_score_distribution, plot_scores_from_csv
from algorithms.depthclimber import DepthClimberRailNetwork
import csv
from algorithms.random_baseline import Baseline
from algorithms.hillclimbrandom import HillClimberRailNetwork
import os

def run_hill_climber_random():
    """
    Runs the Hill Climber Random algorithm and saves the results to a CSV file.
    """
    rail_network = HillClimberRailNetwork(max_time_limit=180)
    rail_network.load_stations("data/NL/StationsNationaal.csv")
    rail_network.load_connections("data/NL/ConnectiesNationaal.csv")
    full_k_scores = []
    real_highst_k = 0
    real_best_traject = None

    with open('Randomhillclimberdata.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["K-score", "Trajectory"])
        
        for i in range(8, 21):
            best_traject, highest_K, k_score_list, trajectory_list = rail_network.hill_climber_optimization(num_iterations=20000, num_routes=i)
            
            # Write each K-score and its corresponding trajectory to the CSV file
            for k_score, trajectory in zip(k_score_list, trajectory_list):
                trajectory_str = ' -> '.join([str(station) for station in trajectory]) 
                writer.writerow([k_score, trajectory_str])
            
            if highest_K > real_highst_k:
                real_highst_k = highest_K
                real_best_traject = best_traject

            full_k_scores += k_score_list

    print("Highest K-Score:", real_highst_k)
    print("Number of Routes used:", len(real_best_traject))
    plot_k_score_distribution(full_k_scores)

def run_greedy(rail_network, stations_file, connections_file):
     # Generate possible trajectories 
    max_duration = 180
    max_stations = 100
    max_reuse = 1
    trajectories = find_trajectories(rail_network, max_duration, max_stations, max_reuse)
     
    # Greedy Algorithm
    greedy = GreedyRouteSelector(rail_network.connections)
    optimized_trajectory_greedy = greedy.greedy_optimization(trajectories)

    # Calculate k score 
    k_score_greedy = calculate_K_score(optimized_trajectory_greedy, rail_network.connections)
    print(f"The K-score for Greedy optimization is: {k_score_greedy}")

    # Print optimized trajectories 
    print("The optimized trajectories are:")
    i = 1 
    for route, duration in optimized_trajectory_greedy:
        print(f"Trajectory {i}: {' -> '.join(route)}, Duration: {duration} minutes")
        print()
        i += 1
    
    # Visualize the final greedy network 
    visualize_network_on_map(rail_network, optimized_trajectory_greedy)

def run_depth_climber(stations_file, connections_file):
    """--- Depth Climber ---"""
    depth_network = DepthClimberRailNetwork(max_time_limit=180)
    depth_network.load_stations(stations_file)
    depth_network.load_connections(connections_file)

    # Setup Depth Climber experiment
    full_k_scores = []
    real_highst_k = 0
    real_best_traject = None

    csv_output_file = 'data/nz-holland/depthclimberdataNZ.csv'
    os.makedirs(os.path.dirname(csv_output_file), exist_ok=True)  # Ensure directory exists
    
    with open(csv_output_file, mode='w', newline='') as file:
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

    # Plot scores from saved CSV file
    plot_scores_from_csv(csv_output_file)

def run_random_baseline():
    """
    Run the random baseline algorithm, save results to a CSV, and plot the K-score distribution.
    """
    # Parameters
    time_limit = 180
    num_trajectories = 260000

    # Initialize the Random baseline
    random_baseline = Baseline(max_time_limit=time_limit)

    # Load stations and connections
    random_baseline.load_stations("data/NL/StationsNationaal.csv")
    random_baseline.load_connections("data/NL/ConnectiesNationaal.csv")

    # Calculate K-scores for the trajectories
    K_scores = random_baseline.calculate_kscore_trajectories(time_limit, num_trajectories)

    # Write K-scores and trajectories to a CSV file
    with open('kscores_trajectories.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['K-Score', 'Trajectory'])  # CSV header

        for trajectory_index in range(num_trajectories):
            # Generate the trajectory and K-score
            traject = random_baseline.generate_random_trajectory(time_limit)
            K_score = K_scores[trajectory_index]
            
            # Convert the trajectory to a string format
            trajectory_str = ' -> '.join(
                ["['{}']".format("', '".join([station.name for station in route])) for route, total_time in traject]
            )
            
            # Write the K-score and trajectory to the CSV file
            writer.writerow([K_score, trajectory_str])

    print(f"{num_trajectories} random trajectories and K-scores have been successfully saved in 'kscores_trajectories.csv'.")

    # Plot the K-score distribution
    plot_k_score_distribution(K_scores)

def main():
    # Load data
    stations_file = 'data/NL/StationsNationaal.csv'
    connections_file = 'data/NL/ConnectiesNationaal.csv'

    # Initialize RailNetwork and load data
    rail_network = RailNetwork(180)
    rail_network.load_stations(stations_file)
    rail_network.load_connections(connections_file)

    # Menu for user selection
    print("Choose which algorithm to run:")
    print("1. Greedy Algorithm")
    print("2. Depth Climber Algorithm")
    print("3. Random Baseline")
    print("4. Hill Climber Random")
    print("5. Run All")
    choice = input("Enter your choice (1/2/3/4/5): ")

    if choice == "1":
        run_greedy(rail_network, stations_file, connections_file)
    elif choice == "2":
        run_depth_climber(stations_file, connections_file)
    elif choice == "3":
        run_random_baseline()
    elif choice == "4":
        run_hill_climber_random()
    elif choice == "5":
        run_greedy(rail_network, stations_file, connections_file)
        run_depth_climber(stations_file, connections_file)
        run_random_baseline()
        run_hill_climber_random()
    else:
        print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")

if __name__ == "__main__":
    main()


