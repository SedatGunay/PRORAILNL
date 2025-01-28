import matplotlib.pyplot as plt
from visualizer import plot_k_score_distribution
from data_loader import load_connections, load_stations
from hillclimbrandom import HillClimberRailNetwork
import csv

import csv
import matplotlib.pyplot as plt
from visualizer import plot_k_score_distribution
from data_loader import load_connections, load_stations
from hillclimbrandom import HillClimberRailNetwork

def main():
    rail_network = HillClimberRailNetwork(max_time_limit=180)
    rail_network.load_stations(r"C:\Users\koste\Documents\GitHub\PRORAILNL\data\NL\StationsNationaal.csv")
    #rail_network.load_stations(r"/Users/sedatgunay/Documents/GitHub/PRORAILNL/data/NL/StationsNationaal.csv")
    rail_network.load_connections(r"C:\Users\koste\Documents\GitHub\PRORAILNL\data\NL\ConnectiesNationaal.csv")
    #rail_network.load_connections(r"/Users/sedatgunay/Documents/GitHub/PRORAILNL/data/NL/ConnectiesNationaal.csv")

    full_k_scores = []
    real_highst_k = 0
    real_best_traject = None

    with open('Randomhillclimberdata.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["K-score", "Trajectory"])
        
        for i in range(2, 21):
            best_traject, highest_K, k_score_list, trajectory_list = rail_network.hill_climber_optimization(num_iterations=10, num_routes=i)
            
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

if __name__ == "__main__":
    main()
