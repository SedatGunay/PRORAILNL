def calculate_K_score(trajectories, connections):
    """
    Calculate the K-score for a list of trajectories.
    """
    used_connections = set()

    for trajectory, total_time in trajectories:
        for i in range(len(trajectory) - 1):
            if hasattr(trajectory[i], 'name') and hasattr(trajectory[i + 1], 'name'):
                # Use name for Station objects 
                connection = tuple(sorted((trajectory[i].name, trajectory[i + 1].name)))
            else:
                # Use strings directly (Greedy)
                connection = tuple(sorted((trajectory[i], trajectory[i + 1])))
            used_connections.add(connection)

    if len(connections) > 0:
        p = len(used_connections) / len(connections)
    else:
        p = 0

    num_trajectories = len(trajectories)
    total_time = sum(trajectory[1] for trajectory in trajectories)

    K_score = p * 10000 - (num_trajectories * 100 + total_time)

    return K_score

