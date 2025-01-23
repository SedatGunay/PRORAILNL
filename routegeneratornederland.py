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


def search(network, current_station, route, current_time, max_duration, max_stations, max_reuse, connection_usage, trajectories, visited):
    """Recursive function to search for valid trajectories."""
    # Only add routes with duration > 0, so we don't add routes with only the starting station.
    if 0 < current_time <= max_duration and len(route) <= max_stations:
        trajectories.add((tuple(route), current_time))

    for connection in network.connections:
        if connection.station1.name == current_station or connection.station2.name == current_station:
            # Check the neighbor station
            neighbor = (connection.station2.name if connection.station1.name == current_station else connection.station1.name)
            time_connection = connection.distance
            connection_name = tuple(sorted((current_station, neighbor)))

            # Check if adding the connection doesn't break conditions
            if current_time + time_connection <= max_duration and connection_usage[connection_name] < max_reuse and neighbor not in visited:
                connection_usage[connection_name] += 1
                visited.add(neighbor)  # Mark the neighbor as visited

                # Continue the search
                search(network, neighbor, route + [neighbor], current_time + time_connection, max_duration, max_stations, max_reuse, connection_usage, trajectories, visited)

                # Backtrack
                visited.remove(neighbor)  # Unmark the neighbor

                connection_usage[connection_name] -= 1

def find_trajectories(network, max_duration, max_stations, max_reuse=1):
    """Finds all possible trajectories constrained by maximum duration, number of stations, and connection reuse."""
    trajectories = set() 
    connection_usage = defaultdict(int)

    # Do for all stations
    start_stations = network.stations.keys()

    for station in start_stations:
        visited = {station}  # Start with the initial station as visited
        search(network, station, [station], 0, max_duration, max_stations, max_reuse, connection_usage, trajectories, visited)

    return list(trajectories)

stations_file = "/Users/sedatgunay/Documents/GitHub/PRORAILNL/data/NL/StationsNationaal.csv"
connections_file = "/Users/sedatgunay/Documents/GitHub/PRORAILNL/data/NL/ConnectiesNationaal.csv"

rail_network = RailNetwork()
rail_network.load_stations(stations_file)
rail_network.load_connections(connections_file)

max_duration = 180
max_stations = 100 
max_reuse = 1

trajectories = find_trajectories(rail_network, max_duration, max_stations, max_reuse)

# Save to a file
with open('trajectories_output4.txt', 'w') as output_file:
    for route, duration in trajectories:
        output_file.write(f"Path: {' -> '.join(route)}, Duration: {duration} minutes\n")
