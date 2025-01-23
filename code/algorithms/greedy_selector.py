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
        selected_routes = []
        unique_used_connections = set()
        total_time_used = 0

        path_data = []
        for path, duration in trajectories:
            if duration <= max_time and duration > 0:
                unique_connections = set(tuple(sorted((path[i], path[i + 1]))) for i in range(len(path) - 1))
                new_connections = unique_connections - unique_used_connections
                used_connections = unique_connections & unique_used_connections

                path_data.append({
                    "path": path,
                    "duration": duration,
                    "new_connections": len(new_connections),
                    "used_connections": len(used_connections),
                    "unique_connections": unique_connections,
                })

        path_data.sort(key=lambda x: (-x["new_connections"], x["used_connections"], x["duration"]))

        for data in path_data:
            if len(selected_routes) >= max_routes:
                break
            if not data["unique_connections"] & unique_used_connections:
                selected_routes.append((data["path"], data["duration"]))
                unique_used_connections.update(data["unique_connections"])
                total_time_used += data["duration"]

        return selected_routes