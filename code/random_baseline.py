import random
import matplotlib.pyplot as plt
import csv
from collections import defaultdict
from classes.rail_network import RailNetwork
from utils.scoring import calculate_K_score

class Baseline(RailNetwork):
    def __init__(self, max_time_limit=None):
        """
        Extends RailNetwork to include a maximum time limit for route searches.
        """
        super().__init__(max_time_limit)
      
    def generate_random_route(self, start_station, time_limit):
        """
        Generate a random route by choosing random valid connection for a given start station and time limit.
        Returns the route and the total time as a tuple.
        """

        num_connections_route = random.randint(1, 20)

        current_station = self.stations[start_station]
        route = [current_station]
        time_route = 0

        for connection in range(num_connections_route):
            connections = self.connection_map[current_station.name]

            if not connections:
                break

            name_next_station, time = random.choice(connections)
            next_station = self.stations[name_next_station]

            if time_route + time > time_limit:
                break
            
            else:
                time_route += time
                route.append(next_station)
                current_station = next_station

        return route, time_route


    def generate_random_trajectory(self, time_limit):
        """
        Generate a random trajectory by generating random routes for a given time limit.
        Returns a list of routes and the total time as a tuple.
        """

        num_routes = random.randint(1, 20)
        routes = []

        # Generate random routes
        for i in range(num_routes):
            start_station = random.choice(list(self.stations.keys()))
            route, total_time = self.generate_random_route(start_station, time_limit)
            routes.append((route, total_time))

        return routes

    def calculate_kscore_trajectories(self, time_limit, num_trajectories):
        """
        Generate and evaluate K-scores of N random trajectories.
        Returns a list of K-scores.
        """

        K_scores = []

        for trajectory in range(num_trajectories):
            print(f"Generating trajectory: {trajectory + 1}")

            traject = self.generate_random_trajectory(time_limit)
            K_score = calculate_K_score(traject, self.connections)
            K_scores.append(K_score)

        return K_scores
