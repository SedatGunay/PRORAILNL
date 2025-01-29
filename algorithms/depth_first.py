from classes.rail_network import RailNetwork

class DepthFirstRailNetwork(RailNetwork):
    def __init__(self, max_time_limit=None):
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