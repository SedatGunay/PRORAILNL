from collections import defaultdict

def search(network, current_station, route, current_time, max_duration, max_stations, max_reuse, connection_usage, trajectories, visited):
    """Recursive function to search for valid trajectories."""
    if 0 < current_time <= max_duration and len(route) <= max_stations:
        trajectories.add((tuple(route), current_time))

    for connection in network.connections:
        if connection.station1.name == current_station or connection.station2.name == current_station:
            neighbor = (connection.station2.name if connection.station1.name == current_station else connection.station1.name)
            time_connection = connection.distance
            connection_name = tuple(sorted((current_station, neighbor)))

            if current_time + time_connection <= max_duration and connection_usage[connection_name] < max_reuse and neighbor not in visited:
                connection_usage[connection_name] += 1
                visited.add(neighbor)

                search(network, neighbor, route + [neighbor], current_time + time_connection, max_duration, max_stations, max_reuse, connection_usage, trajectories, visited)

                visited.remove(neighbor)
                connection_usage[connection_name] -= 1

def find_trajectories(network, max_duration, max_stations, max_reuse=1):
    """Finds all possible trajectories constrained by maximum duration, number of stations, and connection reuse."""
    trajectories = set() 
    connection_usage = defaultdict(int)

    start_stations = network.stations.keys()

    for station in start_stations:
        visited = {station}
        search(network, station, [station], 0, max_duration, max_stations, max_reuse, connection_usage, trajectories, visited)

    return list(trajectories)