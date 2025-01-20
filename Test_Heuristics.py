import csv
from collections import defaultdict
import random

class Station:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

class Connection:
    def __init__(self, station1, station2, distance):
        self.station1 = station1
        self.station2 = station2
        self.distance = distance

class RailNetwork:
    def __init__(self):
        self.stations = {}
        self.connections = []
        self.connection_map = defaultdict(list)

    def load_stations(self, filepath):
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.stations[row['station']] = Station(row['station'], float(row['x']), float(row['y']))

    def load_connections(self, filepath):
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                station1 = row['station1']
                station2 = row['station2']
                distance = int(row['distance'])
                self.connections.append(Connection(station1, station2, distance))
                self.connection_map[station1].append((station2, distance))
                self.connection_map[station2].append((station1, distance))

class Heuristics:
    def __init__(self, rail_network):
        self.rail_network = rail_network
        self.visited_connections = set()
        self.station_visit_count = defaultdict(int)

    def calculate_trajectory_k_score(self, trajectory, total_time):
        trajectory_connections = set(
            (trajectory[i], trajectory[i + 1]) for i in range(len(trajectory) - 1)
        )
        p = len(trajectory_connections) / len(self.rail_network.connections)
        T = 1  # Aantal trajecten is hier altijd 1
        K = p * 10000 - (T * 100 + total_time)
        return K

    def prioritize_unvisited_connections(self, current_station):
        neighbors = self.rail_network.connection_map[current_station]
        neighbors.sort(key=lambda x: ((current_station, x[0]) not in self.visited_connections, x[1]))
        return neighbors

    def apply_heuristics(self, current_station, trajectory, total_time, max_time, max_visits):
        for neighbor_station, time in self.prioritize_unvisited_connections(current_station):
            if self.station_visit_count[neighbor_station] < max_visits and \
               (current_station, neighbor_station) not in self.visited_connections and \
               total_time + time <= max_time:
                return neighbor_station, time
        return None

    def generate_trajectories(self, max_trajectories, max_time, max_visits=2):
        all_trajectories = []
        sorted_stations = sorted(
            self.rail_network.stations.keys(),
            key=lambda s: len(self.rail_network.connection_map[s]),
            reverse=True
        )
        start_stations = sorted_stations[:max_trajectories * 2]

        for start_station in start_stations:
            current_station = start_station
            trajectory = [current_station]
            total_time = 0

            while True:
                next_connection = self.apply_heuristics(
                    current_station, trajectory, total_time, max_time, max_visits
                )
                if next_connection:
                    neighbor_station, time = next_connection
                    trajectory.append(neighbor_station)
                    self.visited_connections.add((current_station, neighbor_station))
                    self.visited_connections.add((neighbor_station, current_station))
                    self.station_visit_count[neighbor_station] += 1
                    total_time += time
                    current_station = neighbor_station
                else:
                    break

            if len(trajectory) > 1:
                k_score = self.calculate_trajectory_k_score(trajectory, total_time)
                all_trajectories.append((trajectory, total_time, k_score))

        best_trajectories = sorted(all_trajectories, key=lambda x: x[2], reverse=True)[:max_trajectories]
        return best_trajectories

if __name__ == "__main__":
    rail_network = RailNetwork()
    rail_network.load_stations("data/NL/StationsNationaal.csv")
    rail_network.load_connections("data/NL/ConnectiesNationaal.csv")

    heuristics = Heuristics(rail_network)

    max_trajectories = 20
    max_time = 180

    best_trajectories = heuristics.generate_trajectories(max_trajectories, max_time)
    print("Top 20 Trajectories with Highest K-Scores:")
    for i, (trajectory, time, k_score) in enumerate(best_trajectories, 1):
        print(f"Trajectory {i}: {' -> '.join(trajectory)} (Total Time: {time} minutes, K-Score: {k_score:.2f})")
