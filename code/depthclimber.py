import copy
import random
from depth_first import DepthFirstRailNetwork
from utils.scoring import calculate_K_score

class DepthClimberRailNetwork(DepthFirstRailNetwork):
    def __init__(self, max_time_limit):
        super().__init__(max_time_limit)

    def generate_initial_trajectories(self, num_trajectories):
        """
        Generate a starting trajectory by generating random routes for a given time limit.
        """
        trajectories = []
        for trajectory in range(num_trajectories):
            start_station_key = random.choice(list(self.stations.keys()))
            start_station = self.stations[start_station_key]

            end_station_key = random.choice(list(self.stations.keys()))
            end_station = self.stations[end_station_key]
            
            routes = self.find_routes(start_station.name, end_station.name, self.max_time_limit)

            # Make sure there are valid routes
            if routes:
                route = random.choice(routes)
                total_time = self.calculate_route_time(route)

                trajectories.append((route, total_time))
        
        return trajectories
    
    def calculate_route_time(self, route):
        """
        Calculate the total time for a given route
        """
        total_time = 0

        for i in range(len(route) - 1):
            current_station = route[i].name
            next_station = route[i + 1].name 

            for next_station_check, time in self.connection_map[current_station]:
                        if next_station_check == next_station:
                            total_time += time
                            break
        return total_time
            
    
    def hill_climber_depth_first(self, num_iterations, initial_trajectories):
        """
        Hill climbing optimization using random chosen depth-first search routes
        """
        trajectory_list = []
        current_trajectory = initial_trajectories
        best_K_score = calculate_K_score(current_trajectory, self.connections)
        k_score_list = [best_K_score]

        for iteration in range(num_iterations):
            new_solution = copy.deepcopy(current_trajectory)
            index_to_replace = random.randint(0, len(new_solution) - 1)
            
            start_station_key = random.choice(list(self.stations.keys()))
            end_station_key = random.choice(list(self.stations.keys()))
            
            possible_routes = self.find_routes(start_station_key, end_station_key, self.max_time_limit)

            if possible_routes:
                new_route = random.choice(possible_routes)
                
                time_new_route = self.calculate_route_time(new_route)
                
                # Update trajectory and recalculate K-score
                new_solution[index_to_replace] = (new_route, time_new_route)
                new_score = calculate_K_score(new_solution, self.connections)
                trajectory_list.append([list(station.name for station in route) for route, _ in new_solution])
                
                k_score_list.append(new_score)
                
                # Check if new solution is better
                if new_score > best_K_score:
                    current_trajectory = new_solution
                    best_K_score = new_score
                    print(f"Iteration {iteration}: Improved K-score to {best_K_score}")

        return current_trajectory, best_K_score, k_score_list,trajectory_list