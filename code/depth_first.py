import copy
import random
import csv
from collections import defaultdict

class Station:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

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
                self.connections.append((station1, station2, distance))
                self.connection_map[station1.name].append((station2.name, distance))
                self.connection_map[station2.name].append((station1.name, distance))

    def depth_first_search(self, current_station, end_station, visited_stations, current_route, current_time, time_limit, routes):
        """
        Depth-first search to find routes between two stations within time limit. Returns a list of routes.
        """

        # Append if completed route
        if current_station == end_station:
            routes.append(current_route.copy())
            return

        # Explore connections
        for next_station_key, connection_time in self.connection_map[current_station.name]:
            next_station = self.stations[next_station_key]
            updated_time = current_time + connection_time

            # Skip if the station is already visited or time limit is exceeded
            if next_station in visited_stations or updated_time > time_limit:
                continue

            visited_stations.add(next_station)
            current_route.append(next_station)

            # Run for updated data
            self.depth_first_search(next_station, end_station, visited_stations, current_route, updated_time, time_limit, routes)

            # Backtrack to try other possible routes
            visited_stations.remove(next_station)
            current_route.pop()


def main():
    rail_network = RailNetwork(max_time_limit=180)
    rail_network.load_stations("StationsHolland.csv")
    rail_network.load_connections("ConnectiesHolland.csv")

if __name__ == "__main__":
    main()