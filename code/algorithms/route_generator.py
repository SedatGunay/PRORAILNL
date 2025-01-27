import csv
from collections import defaultdict

class Station:
    def __init__(self, name, x=None, y=None):
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
        """Loads stations from a CSV file."""
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.stations[row['station']] = Station(row['station'], float(row.get('x', 0)), float(row.get('y', 0)))

    def load_connections(self, filepath):
        """Loads connections from a CSV file."""
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                station1 = self.stations[row['station1']]
                station2 = self.stations[row['station2']]
                distance = int(row['distance'])
                connection = Connection(station1, station2, distance)
                self.connections.append(connection)
                self.connection_map[station1.name].append((station2.name, distance))
                self.connection_map[station2.name].append((station1.name, distance))

def find_trajectories(network, max_duration, max_stations, max_reuse=1):
    """Finds all possible trajectories constrained by maximum duration, number of stations, and connection reuse."""
    trajectories = set()
    connection_usage = defaultdict(int)

    def search(current_station, route, current_time):
        if 0 < current_time <= max_duration and len(route) <= max_stations:
            trajectories.add((tuple(route), current_time))

        for connection in network.connections:
            if connection.station1.name == current_station or connection.station2.name == current_station:
                neighbor = connection.station2.name if connection.station1.name == current_station else connection.station1.name
                time_connection = connection.distance
                connection_name = tuple(sorted((current_station, neighbor)))

                if current_time + time_connection <= max_duration and connection_usage[connection_name] < max_reuse:
                    connection_usage[connection_name] += 1
                    search(neighbor, route + [neighbor], current_time + time_connection)
                    connection_usage[connection_name] -= 1

    for station in network.stations.keys():
        search(station, [station], 0)

    return list(trajectories)
