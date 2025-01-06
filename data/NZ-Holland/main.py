import csv
from collections import defaultdict

class Station:
    def __init__(self, name, x, y):
    # Initialize the  name and coordinates of the station
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

if __name__ == "__main__":
    rail_network = RailNetwork()
    rail_network.load_stations("data/NZ-Holland/StationsHolland.csv")
    rail_network.load_connections("data/NZ-Holland/ConnectiesHolland.csv")
