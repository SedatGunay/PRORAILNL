import csv
from collections import defaultdict

class Station:
    def __init__(self, name, x, y):
        # Initialize the name and coordinates of the station
        self.name = name
        self.x = x
        self.y = y

class Connection:
    def __init__(self, station1, station2, distance):
        # Initialize the stations and the distance between them
        self.station1 = station1
        self.station2 = station2
        self.distance = distance

class RailNetwork:
    def __init__(self):
        self.stations = {}
        self.connections = []
        self.connection_map = defaultdict(list)

    def load_stations(self, filepath):
        # Loop over every station in the datafile 
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.stations[row['station']] = Station(row['station'], float(row['x']), float(row['y']))

    def load_connections(self, filepath):
        # Loop over every connection in the datafile
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                station1 = row['station1']
                station2 = row['station2']
                distance = int(row['distance'])
                self.connections.append(Connection(station1, station2, distance))
                self.connection_map[station1].append((station2, distance))
                self.connection_map[station2].append((station1, distance))

    def greedy_trajectories(self, max_stations, max_time):
        visited_connections = set()
        trajectories = []

        for start_station in self.stations.keys():
            current_station = start_station
            trajectory = [current_station]
            total_time = 0

            while len(trajectory) <= max_stations:
                next_connection = None

                for neighbor_station, time in self.connection_map[current_station]:
                    if (current_station, neighbor_station) not in visited_connections and (neighbor_station, current_station) not in visited_connections:
                        if total_time + time <= max_time:
                            next_connection = (neighbor_station, time)
                            break

                if next_connection:
                    neighbor_station, time = next_connection
                    trajectory.append(neighbor_station)
                    visited_connections.add((current_station, neighbor_station))
                    visited_connections.add((neighbor_station, current_station))
                    total_time += time
                    current_station = neighbor_station
                else:
                    break

            if len(trajectory) > 1:
                trajectories.append((trajectory, total_time))

        return trajectories

if __name__ == "__main__":
    rail_network = RailNetwork()

    # Load data
    rail_network.load_stations("data/NZ-Holland/StationsHolland.csv")
    rail_network.load_connections("data/NZ-Holland/ConnectiesHolland.csv")

    # Run the greedy algorithm
    max_stations = 7
    max_time = 120
    trajectories = rail_network.greedy_trajectories(max_stations, max_time)

    # Output the results of the greedy algorithm
    print("\nGenerated Trajectories:")
    for i, (trajectory, time) in enumerate(trajectories, 1):
        print(f"Trajectory {i}: {' -> '.join(trajectory)} (Total Time: {time} minutes)")
