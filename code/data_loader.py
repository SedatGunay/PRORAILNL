import csv
from classes.station import Station
from classes.connection import Connection

def load_stations(file_path):
    """
    Load station data from a CSV file and create Station objects.

    Args:
        file_path (str): The path to the CSV file containing station data. 

    Returns:
        dict: A dictionary where keys are station names (str) and values are Station objects.
    """
    stations = {}
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            name, y, x = row
            stations[name] = Station(name, float(x), float(y))  # x and y are swapped
    return stations

def load_connections(file_path, stations):
    """
    Load connection data from a CSV file and create Connection objects.

    Args:
        file_path (str): The path to the CSV file containing connection data.
                        The rows must be formatted as: station_name_1, station_name_2, distance
        stations (dict): A dictionary of Station objects, where keys are station names.

    Returns:
        list: A list of Connection objects representing the connections between stations.
    """
    connections = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            station1_name, station2_name, distance = row
            station1 = stations[station1_name]
            station2 = stations[station2_name]
            connection = Connection(station1, station2, float(distance))
            connections.append(connection)
            station1.add_connection(connection)
            station2.add_connection(connection)
    return connections

def load_data(station_file, connection_file):
    """
    Load station and connection data from CSV files.

    Args:
        station_file (str): The path to the CSV file containing station data.
        connection_file (str): The path to the CSV file containing connection data.

    Returns:
        tuple: A tuple containing:
               - stations (dict): A dictionary where keys are station names (str) and values are Station objects.
               - verbindingen (list): A list of Connection objects representing the connections between stations.
    """
    stations = load_stations(station_file)
    connections = load_connections(connection_file, stations)
    return stations, connections
