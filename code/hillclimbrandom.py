import copy
import random
import csv
from collections import defaultdict

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
    def __init__(self, max_time_limit):
        self.stations = {}
        self.connections = []
        self.connection_map = defaultdict(list)
        self.max_time_limit = max_time_limit

    def load_stations(self, filepath):
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.stations[row['station']] = Station(row['station'], float(row['x']), float(row['y']))

    def load_connections(self, filepath):
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                station1 = self.stations[row['station1']]
                station2 = self.stations[row['station2']]
                distance = int(row['distance'])
                self.connections.append(Connection(station1, station2, distance))
                self.connection_map[station1.name].append((station2.name, distance))
                self.connection_map[station2.name].append((station1.name, distance))

    def generate_random_route(self, start_station):
        """
        Generate a random route starting from a station within the time limit.
        """
        current_station = self.stations[start_station]
        route = [current_station]
        time_route = 0

        max_connections = random.randint(2, 50)

        for connection_n in range(max_connections):
            connections = self.connection_map[current_station.name]
            
            if not connections:
                break

            next_station_key, time = random.choice(connections)
            next_station = self.stations[next_station_key]

            if time_route + time > self.max_time_limit:
                break
            
            time_route += time
            route.append(next_station)
            current_station = next_station

        return route, time_route

    def calculate_K_score(self, trajectories):
        """
        Calculate the K-score for a list of trajectories
        """
        used_connections = set()

        for trajectory, total_time in trajectories:
            for i in range(len(trajectory) - 1):
                connection = tuple(sorted((trajectory[i].name, trajectory[i + 1].name)))
                used_connections.add(connection)

        if len(self.connections) > 0:
            p = len(used_connections) / len(self.connections)
        else:
            p = 0

        num_trajectories = len(trajectories)
        total_time = sum(trajectory[1] for trajectory in trajectories)

        K_score = p * 10000 - (num_trajectories * 100 + total_time)

        return K_score

# Example usage
def main():
    rail_network = RailNetwork(max_time_limit=180)
    rail_network.load_stations("StationsHolland.csv")
    rail_network.load_connections("ConnectiesHolland.csv")

if __name__ == "__main__":
    main()