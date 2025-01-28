import matplotlib.pyplot as plt
from visualizer import plot_k_score_distribution
from data_loader import load_connections, load_stations
from hillclimbrandom import HillClimberRailNetwork

def main():
    rail_network = HillClimberRailNetwork(max_time_limit=180)
    # rail_network.load_stations(r"C:\Users\koste\Documents\GitHub\PRORAILNL\data\NL\StationsNationaal.csv")
    rail_network.load_stations(r"/Users/sedatgunay/Documents/GitHub/PRORAILNL/data/NL/StationsNationaal.csv")
    # rail_network.load_connections(r"C:\Users\koste\Documents\GitHub\PRORAILNL\data\NL\ConnectiesNationaal.csv")
    rail_network.load_connections(r"/Users/sedatgunay/Documents/GitHub/PRORAILNL/data/NL/ConnectiesNationaal.csv")

    # Setup for the experiment
    full_k_scores = []
    real_highst_k = 0
    real_best_traject = None

    for i in range(2, 21):
        best_traject, highest_K, k_score_list = rail_network.hill_climber_optimization(num_iterations=1000, num_routes=i) 
        if highest_K > real_highst_k:
            real_highst_k = highest_K
            real_best_traject = best_traject

        full_k_scores += k_score_list

    print("Highest K-Score:", real_highst_k)
    print("Number of Routes used:", len(real_best_traject))

    plot_k_score_distribution(full_k_scores)

if __name__ == "__main__":
    main()