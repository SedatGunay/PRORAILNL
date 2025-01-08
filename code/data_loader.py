import csv
from greedy import Station, Verbinding  

""" Code om csv bestanden te laden"""

def load_stations(file_path):
    stations = {}
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            name, y, x = row
            stations[name] = Station(name, float(x), float(y))  # x en y zijn omgedraaid
    return stations

def load_connections(file_path, stations):
    verbindingen = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            station1_name, station2_name, distance = row
            station1 = stations[station1_name]
            station2 = stations[station2_name]
            verbinding = Verbinding(station1, station2, float(distance))
            verbindingen.append(verbinding)
            station1.add_verbinding(verbinding)
            station2.add_verbinding(verbinding)
    return verbindingen

def load_data(station_file, connection_file):
    stations = load_stations(station_file)
    verbindingen = load_connections(connection_file, stations)
    return stations, verbindingen