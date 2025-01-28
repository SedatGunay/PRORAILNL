import random
import matplotlib.pyplot as plt
import csv
from random_baseline import Random
from utils.scoring import calculate_K_score


time_limit = 180 
num_trajectories = 260000

random_baseline = Random(max_time_limit=time_limit)

# Laad de stations en verbindingen (pas het pad aan naar je bestanden)
random_baseline.load_stations("data/NL/StationsNationaal.csv")
random_baseline.load_connections("data/NL/ConnectiesNationaal.csv")

K_scores = random_baseline.calculate_kscore_trajectories(time_limit, num_trajectories)

# Schrijf de K-scores en de trajecten naar een CSV-bestand
with open('kscores_trajectories.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['K-Score', 'Trajectory'])  # Header

    for trajectory in range(num_trajectories):
        # Genereer het traject en de K-score
        traject = random_baseline.generate_random_trajectory(time_limit)
        K_score = K_scores[trajectory]
        
        trajectory_str = ' -> '.join(
            ["['{}']".format("', '".join([station.name for station in route])) for route, total_time in traject]
        )
        
        writer.writerow([K_score, trajectory_str])

print(f"{num_trajectories} random trajecten en K-scores zijn succesvol opgeslagen in 'kscores_trajectories.csv'.")

# Plot de distributie van de K-scores
plt.hist(K_scores, bins=100, edgecolor='black')
plt.title("K-Score Distribution")
plt.xlabel("K-Score")
plt.ylabel("Frequency")
plt.grid(True)
plt.show()
