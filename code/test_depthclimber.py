from depthclimber import DepthClimberRailNetwork
import matplotlib.pyplot as plt
from visualizer import plot_k_score_distribution
import csv

def main():
    rail_network = DepthClimberRailNetwork(max_time_limit=180)
    rail_network.load_stations(r"C:\Users\koste\Documents\GitHub\PRORAILNL\data\NL\StationsNationaal.csv")
    rail_network.load_connections(r"C:\Users\koste\Documents\GitHub\PRORAILNL\data\NL\ConnectiesNationaal.csv")
    
    full_k_scores = []
    real_highst_k = 0
    real_best_traject = None

    with open('depthclimberdata.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['K-Score', 'Trajectory'])
        
        for i in range(2, 21):
            initial_trajectories = rail_network.generate_initial_trajectories(num_trajectories=i)
            best_trajectory, best_K_score, k_score_list, trajectory_list = rail_network.hill_climber_depth_first(num_iterations=1, initial_trajectories=initial_trajectories)
        
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

if __name__ == "__main__":
    main()