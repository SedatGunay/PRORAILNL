import random
import matplotlib.pyplot as plt
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
                station1 = self.stations[row['station1']]
                station2 = self.stations[row['station2']]
                distance = int(row['distance'])
                self.connections.append(Connection(station1, station2, distance))
                self.connection_map[station1.name].append((station2.name, distance))
                self.connection_map[station2.name].append((station1.name, distance))

    def generate_random_route(self, start_station, time_limit):
        """
        Generate a random route by choosing random valid connection for a given start station and time limit.
        Returns the route and the total time as a tuple.
        """

        num_connections_route = random.randint(1, 20)

        current_station = self.stations[start_station]
        route = [current_station]
        time_route = 0

        for connection in range(num_connections_route):
            connections = self.connection_map[current_station.name]

            if not connections:
                break

            name_next_station, time = random.choice(connections)
            next_station = self.stations[name_next_station]

            if time_route + time > time_limit:
                break
            
            else:
                time_route += time
                route.append(next_station)
                current_station = next_station

        return route, time_route


    def generate_random_trajectory(self, time_limit):
        """
        Generate a random trajectory by generating random routes for a given time limit.
        Returns a list of routes and the total time as a tuple.
        """

        num_routes = random.randint(1, 20)
        routes = []

        # Generate random routes
        for i in range(num_routes):
            start_station = random.choice(list(self.stations.keys()))
            route, total_time = self.generate_random_route(start_station, time_limit)
            routes.append((route, total_time))

        return routes

    def calculate_kscore_trajectories(self, time_limit, num_trajectories):
        """
        Generate and evaluate K-scores of N random trajectories.
        Returns a list of K-scores.
        """

        K_scores = []

        for trajectory in range(num_trajectories):
            print(f"Generating trajectory: {trajectory + 1}")

            traject = self.generate_random_trajectory(time_limit)
            K_score = self.calculate_K_score(traject)
            K_scores.append(K_score)

        return K_scores
    
    
    def calculate_K_score(self, trajectories):
        """
        Calculate the K-score for a list of trajectories.
        """
        # Look at unique connections
        used_connections = set()

        for trajectory, total_time in trajectories:
            for i in range(len(trajectory) - 1):
                # Sort station names to avoid duplicates
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


rail_network = RailNetwork()
rail_network.load_stations("/Users/sedatgunay/Documents/GitHub/PRORAILNL/data/NL/StationsNationaal.csv")
rail_network.load_connections("/Users/sedatgunay/Documents/GitHub/PRORAILNL/data/NL/ConnectiesNationaal.csv")

time_limit = 180 
num_trajectories = 100000 

# Generate and evaluate N random trajectories
K_scores = rail_network.calculate_kscore_trajectories(time_limit, num_trajectories)

# Plot the distribution of K-scores
plt.hist(K_scores,edgecolor='black', bins=100)

plt.title("K-Score Distribution")
plt.xlabel("K-Score")
plt.ylabel("Frequency")
plt.grid(True)

plt.show()
