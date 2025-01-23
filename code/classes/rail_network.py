from collections import defaultdict
from classes.station import Station
from classes.connection import Connection
from data_loader import load_stations, load_connections

class RailNetwork:
    def __init__(self):
        self.stations = {}
        self.connections = []
        self.connection_map = defaultdict(list)

    def load_data(self, station_file, connection_file):
        """Loads stations and connections from CSV files."""
        self.stations = load_stations(station_file)
        self.connections = load_connections(connection_file, self.stations)