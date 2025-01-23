class GreedyRouteSelector:
    def __init__(self, connections):
        self.connections = connections

    def calculate_K_score(self, trajectories):
        unique_used_connections = set()
        for trajectory, _ in trajectories:
            for i in range(len(trajectory) - 1):
                unique_used_connections.add(tuple(sorted((trajectory[i], trajectory[i + 1]))))
        total_connections = len(self.connections)

        p = len(unique_used_connections) / total_connections
        T = len(trajectories)
        Min = sum(total_time for _, total_time in trajectories)
        return p * 10000 - (T * 100 + Min)

    def greedy_optimization(self, trajectories, max_routes=20, max_time=180, first_path_index=0):
        """
        Optimize the selection of paths based on maximizing unused connections,
        minimizing already used connections, and minimizing total time.
        """
        selected_routes = []
        unique_used_connections = set()
        total_time_used = 0
        selected_paths_set = set()

        path_data = []
        for path, duration in trajectories:
            if duration <= max_time and duration > 0: # DIT KAN AANGEPAST WORDEN VANWEGE AANPASSINGEN IN HET ROUTE GENERATIE ALGORITME
                unique_connections = set(tuple(sorted((path[i], path[i + 1]))) for i in range(len(path) - 1))

                # Determine new and used connections
                new_connections = unique_connections - unique_used_connections
                used_connections = unique_connections & unique_used_connections

                # Add trajectory info
                path_data.append({
                    "path": path,
                    "duration": duration,
                    "new_connections": len(new_connections),
                    "used_connections": len(used_connections),
                    "unique_connections": unique_connections,})

        # Sort paths by chosen greedy criteria
        path_data.sort(key=lambda x: (-x["new_connections"], x["used_connections"], x["duration"]))

        # Check if list of paths is long enough to select the first path with chosen index
        if path_data and first_path_index < len(path_data):
            first_path = path_data[first_path_index]
            selected_routes.append((first_path["path"], first_path["duration"]))
            unique_used_connections.update(first_path["unique_connections"])
            selected_paths_set.add(tuple(first_path["path"]))
            total_time_used += first_path["duration"]

        # Continue searching for other routes
        for data in path_data:
            # Stop early if we have enough routes
            if len(selected_routes) >= max_routes:
                break

            path, duration, unique_connections = data["path"], data["duration"], data["unique_connections"]

            # Dont use duplicate paths
            if tuple(path) in selected_paths_set:
                continue

            if total_time_used + duration <= max_routes * max_time:
                # Add the path only if it introduces new connections and does not reuse connections
                if not unique_connections & unique_used_connections:
                    selected_routes.append((path, duration))
                    unique_used_connections.update(unique_connections)
                    selected_paths_set.add(tuple(path))
                    total_time_used += duration

            # Stop if all connections are used
            if len(unique_used_connections) == len(self.connections):
                break

        return selected_routes



# Connections that need to be covered for early stopage
connections = {
    ("Alkmaar", "Hoorn"),
    ("Alkmaar", "Den Helder"),
    ("Almelo", "Hengelo"),
    ("Almere Centrum", "Lelystad Centrum"),
    ("Amsterdam Amstel", "Almere Centrum"),
    ("Amsterdam Amstel", "Amsterdam Centraal"),
    ("Amsterdam Amstel", "Amsterdam Zuid"),
    ("Amsterdam Amstel", "Hilversum"),
    ("Amsterdam Centraal", "Almere Centrum"),
    ("Amsterdam Centraal", "Amsterdam Sloterdijk"),
    ("Amsterdam Sloterdijk", "Haarlem"),
    ("Amsterdam Sloterdijk", "Zaandam"),
    ("Amsterdam Zuid", "Schiphol Airport"),
    ("Amsterdam Zuid", "Amsterdam Sloterdijk"),
    ("Apeldoorn", "Amersfoort"),
    ("Apeldoorn", "Zutphen"),
    ("Arnhem Centraal", "Ede-Wageningen"),
    ("Arnhem Centraal", "Dieren"),
    ("Assen", "Zwolle"),
    ("Beverwijk", "Castricum"),
    ("Breda", "Etten-Leur"),
    ("Breda", "Dordrecht"),
    ("Castricum", "Alkmaar"),
    ("Delft", "Den Haag Laan v NOI"),
    ("Delft", "Den Haag Centraal"),
    ("Delft", "Den Haag HS"),
    ("Den Haag Centraal", "Gouda"),
    ("Den Haag Centraal", "Leiden Centraal"),
    ("Den Haag HS", "Gouda"),
    ("Den Haag HS", "Leiden Centraal"),
    ("Den Haag Laan v NOI", "Leiden Centraal"),
    ("Den Haag Laan v NOI", "Gouda"),
    ("Deventer", "Apeldoorn"),
    ("Deventer", "Almelo"),
    ("Deventer", "Zutphen"),
    ("Dordrecht", "Rotterdam Centraal"),
    ("Dordrecht", "Rotterdam Blaak"),
    ("Eindhoven", "Helmond"),
    ("Eindhoven", "s-Hertogenbosch"),
    ("Eindhoven", "Tilburg"),
    ("Etten-Leur", "Roosendaal"),
    ("Gouda", "Alphen a/d Rijn"),
    ("Groningen", "Assen"),
    ("Haarlem", "Beverwijk"),
    ("Heemstede-Aerdenhout", "Haarlem"),
    ("Heerenveen", "Steenwijk"),
    ("Helmond", "Venlo"),
    ("Hengelo", "Enschede"),
    ("Hilversum", "Almere Centrum"),
    ("Leeuwarden", "Heerenveen"),
    ("Leeuwarden", "Groningen"),
    ("Leiden Centraal", "Schiphol Airport"),
    ("Leiden Centraal", "Alphen a/d Rijn"),
    ("Leiden Centraal", "Heemstede-Aerdenhout"),
    ("Maastricht", "Sittard"),
    ("Nijmegen", "Arnhem Centraal"),
    ("Oss", "Nijmegen"),
    ("Roermond", "Weert"),
    ("Roosendaal", "Vlissingen"),
    ("Roosendaal", "Dordrecht"),
    ("Rotterdam Alexander", "Gouda"),
    ("Rotterdam Blaak", "Rotterdam Alexander"),
    ("Rotterdam Blaak", "Schiedam Centrum"),
    ("Rotterdam Centraal", "Rotterdam Alexander"),
    ("Rotterdam Centraal", "Schiedam Centrum"),
    ("Schiedam Centrum", "Delft"),
    ("Sittard", "Heerlen"),
    ("Sittard", "Roermond"),
    ("Steenwijk", "Zwolle"),
    ("Tilburg", "Breda"),
    ("Utrecht Centraal", "Amsterdam Centraal"),
    ("Utrecht Centraal", "Amsterdam Amstel"),
    ("Utrecht Centraal", "Hilversum"),
    ("Utrecht Centraal", "Ede-Wageningen"),
    ("Utrecht Centraal", "Amersfoort"),
    ("Utrecht Centraal", "Gouda"),
    ("Utrecht Centraal", "Alphen a/d Rijn"),
    ("Utrecht Centraal", "Schiphol Airport"),
    ("Utrecht Centraal", "s-Hertogenbosch"),
    ("Weert", "Eindhoven"),
    ("Zaandam", "Hoorn"),
    ("Zaandam", "Castricum"),
    ("Zaandam", "Beverwijk"),
    ("Zutphen", "Dieren"),
    ("Zwolle", "Amersfoort"),
    ("Zwolle", "Deventer"),
    ("Zwolle", "Almelo"),
    ("s-Hertogenbosch", "Oss"),
    ("s-Hertogenbosch", "Tilburg")
}

connectiesNZ ={
    ("Alkmaar", "Hoorn"),
    ("Alkmaar", "Den Helder"),
    ("Amsterdam Amstel", "Amsterdam Zuid"),
    ("Amsterdam Amstel", "Amsterdam Centraal"),
    ("Amsterdam Centraal", "Amsterdam Sloterdijk"),
    ("Amsterdam Sloterdijk", "Haarlem"),
    ("Amsterdam Sloterdijk", "Zaandam"),
    ("Amsterdam Zuid", "Amsterdam Sloterdijk"),
    ("Amsterdam Zuid", "Schiphol Airport"),
    ("Beverwijk", "Castricum"),
    ("Castricum", "Alkmaar"),
    ("Delft", "Den Haag Centraal"),
    ("Den Haag Centraal", "Gouda"),
    ("Den Haag Centraal", "Leiden Centraal"),
    ("Dordrecht", "Rotterdam Centraal"),
    ("Gouda", "Alphen a/d Rijn"),
    ("Haarlem", "Beverwijk"),
    ("Heemstede-Aerdenhout", "Haarlem"),
    ("Leiden Centraal", "Heemstede-Aerdenhout"),
    ("Leiden Centraal", "Alphen a/d Rijn"),
    ("Leiden Centraal", "Schiphol Airport"),
    ("Rotterdam Alexander", "Gouda"),
    ("Rotterdam Centraal", "Schiedam Centrum"),
    ("Rotterdam Centraal", "Rotterdam Alexander"),
    ("Schiedam Centrum", "Delft"),
    ("Zaandam", "Castricum"),
    ("Zaandam", "Beverwijk"),
    ("Zaandam", "Hoorn")
}

# Read trajectories from the file
def read_trajectories(file_path):
    trajectories = []

    with open(file_path, 'r') as file:
        for line in file:
            # Remove fluff 
            parts = line.strip().split(", Duration: ")
            path = parts[0].replace("Path: ", "").split(" -> ")
            duration = int(parts[1].replace(" minutes", ""))
            trajectories.append((path, duration))
    return trajectories

trajectories_file = "trajectories_output2.txt"
trajectories = read_trajectories(trajectories_file)

selector = GreedyRouteSelector(connections)

highest_K_score = 0
best_routes = None

# Run the algo multiple times with a different first path index to get different results
for i in range(200):
    print(i)
    optimized_paths_first_run = selector.greedy_optimization(trajectories, first_path_index=i)
    final_score_first_run = selector.calculate_K_score(optimized_paths_first_run)

    if final_score_first_run > highest_K_score:
        print("Highest K score:", final_score_first_run)
        highest_K_score = final_score_first_run
        best_routes = optimized_paths_first_run
        print("Best routes:", best_routes)
