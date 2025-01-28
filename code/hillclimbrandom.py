import copy
import random
from classes.rail_network import RailNetwork
from utils.scoring import calculate_K_score

class HillClimberRailNetwork(RailNetwork):
    def __init__(self, max_time_limit):
        super().__init__(max_time_limit)

    def generate_random_route(self, start_station):
        """
        Generate a random route starting from a station within the time limit.
        """
        current_station = self.stations[start_station]
        route = [current_station]
        time_route = 0

        max_connections = random.randint(2, 50)

        for connection_n in range(max_connections):
            connections = self.connection_map[current_station.name]
            
            if not connections:
                break

            next_station_key, time = random.choice(connections)
            next_station = self.stations[next_station_key]

            if time_route + time > self.max_time_limit:
                break
            
            time_route += time
            route.append(next_station)
            current_station = next_station

        return route, time_route

    def generate_random_trajectory(self, num_routes):
        """
        Generate a random set of a random amount of routes.
        """
        routes = []

        for route_n in range(num_routes):
            start_station = random.choice(list(self.stations.keys()))
            route, total_time = self.generate_random_route(start_station)
            routes.append((route, total_time))

        return routes
    
    def swap_routes(self, trajectories):
        """
        Change a random amount of routes in a list of trajectories.
        """
        trajectories_copy = copy.deepcopy(trajectories)
        
        # Randomly select num routes to replace but limit to half of the total routes
        num_replace = random.randint(1, len(trajectories_copy) // 2)
        
        for _ in range(num_replace):
            index_to_replace = random.randint(0, len(trajectories_copy) - 1)

            start_station = random.choice(list(self.stations.keys()))
            new_route, new_time = self.generate_random_route(start_station)

            trajectories_copy[index_to_replace] = (new_route, new_time)

        return trajectories_copy
    
    def hill_climber_optimization(self, num_iterations, num_routes=10):
        """
        Hill climber optimization algorithm to find the best set of trajectories.
        """
        trajectory_list = []
        best_routes = self.generate_random_trajectory(num_routes)
        best_K_score = calculate_K_score(best_routes, self.connections)
        k_score_list = [best_K_score]

        for iteration in range(num_iterations):
            updated_trajectory = self.swap_routes(best_routes)
            updated_K_score = calculate_K_score(updated_trajectory, self.connections)

            trajectory_list.append([list(station.name for station in route) for route, _ in updated_trajectory])

            k_score_list.append(updated_K_score)

            if updated_K_score > best_K_score:
                best_routes = updated_trajectory
                best_K_score = updated_K_score

                print(f"Iteration: {iteration}, K-Score: {best_K_score}")

        return best_routes, best_K_score, k_score_list, trajectory_list