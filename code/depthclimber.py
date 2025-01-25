import copy
import random
import csv
from collections import defaultdict
import matplotlib.pyplot as plt

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

    def find_routes(self, start_station_key, end_station_key, time_limit):
        """
        Find routes between two stations within a time limit.
        """
        
        start_station = self.stations[start_station_key]
        end_station = self.stations[end_station_key]

        routes = []
        self.depth_first_search(start_station, end_station, {start_station}, [start_station], 0, time_limit, routes)
        return routes

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

            # make sure there are valid routes
            if routes:
                route = random.choice(routes)
                total_time = 0

                # DIT KAN NOG ERGENS VERBETERD WORDEN IN EEN LOSSE FUNCTIE
                for i in range(len(route) - 1):
                    current_station = route[i].name
                    next_station = route[i + 1].name

                    for next_station_check, time in self.connection_map[current_station]:
                        if next_station_check == next_station:
                            total_time += time
                            break

                trajectories.append((route, total_time))
        
        return trajectories
    
    def hill_climber_depth_first(self, num_iterations, initial_trajectories):
        """
        Hill climbing optimization using random chosen depth-first search routes
        """


        
        current_trajectory = initial_trajectories
        best_K_score = self.calculate_K_score(current_trajectory)
        k_score_list = [best_K_score]

        for iteration in range(num_iterations):
            new_solution = copy.deepcopy(current_trajectory)
            index_to_replace = random.randint(0, len(new_solution) - 1)
            
            start_station_key = random.choice(list(self.stations.keys()))
            start_station = self.stations[start_station_key]
            
            end_station_name = random.choice(list(self.stations.keys()))
            end_station = self.stations[end_station_name]
            
            possible_routes = self.find_routes(start_station.name, end_station.name, self.max_time_limit)

            if possible_routes:
                new_route = random.choice(possible_routes)
                
                # DIT KAN NOG ERGENS VERBETERD WORDEN IN EEN LOSSE FUNCTIE
                time_new_route = 0
                for i in range(len(new_route) - 1):
                    current_station = new_route[i].name
                    next_station = new_route[i + 1].name
                    
                    for next_station_name, dist in self.connection_map[current_station]:
                        if next_station_name == next_station:
                            time_new_route += dist
                            break
                
                # Update trajectory and recaculate K-score
                new_solution[index_to_replace] = (new_route, time_new_route)
                new_score = self.calculate_K_score(new_solution)
                
                k_score_list.append(new_score)
                
                # Check if new solution is better
                if new_score > best_K_score:
                    current_trajectory = new_solution
                    best_K_score = new_score
                    print(f"Iteration {iteration}: Improved K-score to {best_K_score}")

        return current_trajectory, best_K_score, k_score_list

    def calculate_K_score(self, trajectories):
        """
        Calculate the K-score for a list of trajectories
        """
        used_connections = set()

        for trajectory, total_time in trajectories:
            for i in range(len(trajectory) - 1):
                connection = tuple(sorted((trajectory[i].name, trajectory[i + 1].name)))
                used_connections.add(connection)

        if len(self.connections) > 0:
            p = len(used_connections) / len(self.connections)
        else:
            p = 0

        num_trajectories = len(trajectories)
        total_time = sum(trajectory[1] for trajectory in trajectories)

        K_score = p * 10000 - (num_trajectories * 100 + total_time)

        return K_score
    
def main():
    rail_network = RailNetwork(max_time_limit=180)
    rail_network.load_stations(r"C:\Users\koste\Documents\GitHub\PRORAILNL\data\NL\StationsNationaal.csv")
    rail_network.load_connections(r"C:\Users\koste\Documents\GitHub\PRORAILNL\data\NL\ConnectiesNationaal.csv")
    
    # Setup for the experiment
    full_k_scores = []
    real_highst_k = 0
    real_best_traject = None

    for i in range(2, 21):
        initial_trajectories = rail_network.generate_initial_trajectories(num_trajectories=i)
        best_trajectory, best_K_score, k_score_list = rail_network.hill_climber_depth_first(num_iterations=1000, initial_trajectories=initial_trajectories)
        if best_K_score > real_highst_k:
            real_highst_k = best_K_score
            real_best_traject = best_trajectory

        full_k_scores += k_score_list

    print("Highest K-Score:", real_highst_k)
    print("Number of Routes used:", len(real_best_traject))
    print("Highest K-Score:", best_K_score)
    print("Number of Routes used:", len(best_trajectory))

    plt.hist(k_score_list,edgecolor='black', bins=20)

    plt.title("K-Score Distribution")
    plt.xlabel("K-Score")
    plt.ylabel("Frequency")
    plt.grid(True)

    plt.show()

if __name__ == "__main__":
    main()