from depthclimber import DepthClimberRailNetwork
import matplotlib.pyplot as plt

def main():
    rail_network = DepthClimberRailNetwork(max_time_limit=180)
    rail_network.load_stations(r"/Users/sedatgunay/Documents/GitHub/PRORAILNL/data/NL/StationsNationaal.csv")
    rail_network.load_connections(r"/Users/sedatgunay/Documents/GitHub/PRORAILNL/data/NL/ConnectiesNationaal.csv")
    
    # Setup for the experiment
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

    plt.hist(full_k_scores, edgecolor='black', bins=20)

    plt.title("K-Score Distribution")
    plt.xlabel("K-Score")
    plt.ylabel("Frequency")
    plt.grid(True)

    plt.show()

if __name__ == "__main__":
    main()