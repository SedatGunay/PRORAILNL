from classes.station import Station
from classes.connection import Connection
from classes.rail_network import RailNetwork

class DepthFirstRailNetwork(RailNetwork):
    def __init__(self, max_time_limit=None):
        """
        Extends RailNetwork to include a maximum time limit for route searches.
        """
        super().__init__(max_time_limit)

    def depth_first_search(self, current_station, end_station, visited_stations, current_route, current_time, routes):
        """
        Depth-first search to find routes between two stations within the max time limit.
        """

        # Append the route if it reaches the destination
        if current_station == end_station:
            routes.append(current_route.copy())
            return

        # Explore all connected stations
        for next_station_key, connection_time in self.connection_map[current_station.name]:
            next_station = self.stations[next_station_key]
            updated_time = current_time + connection_time

            # Skip if the station is already visited or exceeds the time limit
            if next_station in visited_stations or (self.max_time_limit and updated_time > self.max_time_limit):
                continue

            visited_stations.add(next_station)
            current_route.append(next_station)

            # Recursive call to continue the depth-first search
            self.depth_first_search(next_station, end_station, visited_stations, current_route, updated_time, routes)

            # Backtrack to explore other routes
            visited_stations.remove(next_station)
            current_route.pop()

    def find_routes(self, start_station_key, end_station_key, time_limit=None):
        """
        Finds all routes between two stations within the max time limit.
        """
        if start_station_key not in self.stations or end_station_key not in self.stations:
            raise ValueError("Sttarting station or end station not in stations.")
        
        time_limit = time_limit if time_limit is not None else self.max_time_limit

        start_station = self.stations[start_station_key]
        end_station = self.stations[end_station_key]

        routes = []
        self.depth_first_search(start_station, end_station, {start_station}, [start_station], 0,routes)
        return routes
    
def main():
    rail_network = DepthFirstRailNetwork(max_time_limit=180)
    rail_network.load_stations(r"/Users/sedatgunay/Documents/GitHub/PRORAILNL/data/NL/StationsNationaal.csv")
    rail_network.load_connections(r"/Users/sedatgunay/Documents/GitHub/PRORAILNL/data/NL/ConnectiesNationaal.csv")
    
    # Test
    start_station = "Amsterdam Centraal"
    end_station = "Rotterdam Centraal"

    time_limit = 180

    routes = rail_network.find_routes(start_station, end_station, time_limit)
    print(len(routes))


if __name__ == "__main__":
    main()




# import copy
# import random
# import csv
# from collections import defaultdict

# class Station:

#     def __init__(self, name, x, y):
#         self.name = name
#         self.x = x
#         self.y = y

# class RailNetwork:

#     def __init__(self, max_time_limit):
#         self.stations = {}
#         self.connections = []
#         self.connection_map = defaultdict(list)
#         self.max_time_limit = max_time_limit

#     def load_stations(self, filepath):
#         with open(filepath, 'r') as file:
#             reader = csv.DictReader(file)
#             for row in reader:
#                 self.stations[row['station']] = Station(row['station'], float(row['x']), float(row['y']))

#     def load_connections(self, filepath):
#         with open(filepath, 'r') as file:
#             reader = csv.DictReader(file)
#             for row in reader:
#                 station1 = self.stations[row['station1']]
#                 station2 = self.stations[row['station2']]
#                 distance = int(row['distance'])
#                 self.connections.append((station1, station2, distance))
#                 self.connection_map[station1.name].append((station2.name, distance))
#                 self.connection_map[station2.name].append((station1.name, distance))

#     def depth_first_search(self, current_station, end_station, visited_stations, current_route, current_time, time_limit, routes):
#         """
#         Depth-first search to find routes between two stations within time limit. Returns a list of routes.
#         """

#         # Append if completed route
#         if current_station == end_station:
#             routes.append(current_route.copy())
#             return

#         # Explore connections
#         for next_station_key, connection_time in self.connection_map[current_station.name]:
#             next_station = self.stations[next_station_key]
#             updated_time = current_time + connection_time

#             # Skip if the station is already visited or time limit is exceeded
#             if next_station in visited_stations or updated_time > time_limit:
#                 continue

#             visited_stations.add(next_station)
#             current_route.append(next_station)

#             # Run for updated data
#             self.depth_first_search(next_station, end_station, visited_stations, current_route, updated_time, time_limit, routes)

#             # Backtrack to try other possible routes
#             visited_stations.remove(next_station)
#             current_route.pop()

#     def find_routes(self, start_station_key, end_station_key, time_limit):
#         """
#         Find routes between two stations within a time limit.
#         """
        
#         start_station = self.stations[start_station_key]
#         end_station = self.stations[end_station_key]

#         routes = []
#         self.depth_first_search(start_station, end_station, {start_station}, [start_station], 0, time_limit, routes)
#         return routes

# def main():

#     rail_network = RailNetwork(max_time_limit=180)
#     # rail_network.load_stations(r"C:\Users\koste\Documents\GitHub\PRORAILNL\data\NL\StationsNationaal.csv")
#     # rail_network.load_connections(r"C:\Users\koste\Documents\GitHub\PRORAILNL\data\NL\ConnectiesNationaal.csv")
#     rail_network.load_stations(r"/Users/sedatgunay/Documents/GitHub/PRORAILNL/data/NL/StationsNationaal.csv")
#     rail_network.load_connections(r"/Users/sedatgunay/Documents/GitHub/PRORAILNL/data/NL/ConnectiesNationaal.csv")
#     # Test
#     start_station = "Amsterdam Centraal"
#     end_station = "Rotterdam Centraal"

#     time_limit = 180

#     routes = rail_network.find_routes(start_station, end_station, time_limit)
#     print(len(routes))

# if __name__ == "__main__":
#     main()