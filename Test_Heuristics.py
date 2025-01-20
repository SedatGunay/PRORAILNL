import csv
from collections import defaultdict
import random

class Station:
    # Klasse om een station te representeren met naam en coördinaten
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

class Connection:
    # Klasse om een verbinding tussen twee stations te representeren met afstand
    def __init__(self, station1, station2, distance):
        self.station1 = station1
        self.station2 = station2
        self.distance = distance

class RailNetwork:
    # Klasse voor het bijhouden van stations, verbindingen en een mapping voor snel zoeken
    def __init__(self):
        self.stations = {}
        self.connections = []
        self.connection_map = defaultdict(list)

    def load_stations(self, filepath):
        # Laad stationsdata vanuit een CSV-bestand
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Maak een Station-object en voeg het toe aan de stationslijst
                self.stations[row['station']] = Station(row['station'], float(row['x']), float(row['y']))

    def load_connections(self, filepath):
        # Laad verbindingen tussen stations vanuit een CSV-bestand
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                station1 = row['station1']
                station2 = row['station2']
                distance = int(row['distance'])

                # Voeg een Connection-object toe en update de mapping
                self.connections.append(Connection(station1, station2, distance))
                self.connection_map[station1].append((station2, distance))
                self.connection_map[station2].append((station1, distance))

class Heuristics:
    # Klasse om heuristieken en K-score berekeningen te doen
    def __init__(self, rail_network):
        self.rail_network = rail_network

        # Houd bij welke verbindingen al bezocht zijn
        self.visited_connections = set()

        # Houd bij hoe vaak een station bezocht is
        self.station_visit_count = defaultdict(int)

    def prevent_single_connection_trajectories(self, trajectory):
        # Zorg ervoor dat een traject meer dan één station bevat
        return len(trajectory) > 1

    def limit_max_time_per_trajectory(self, trajectory_time, max_time):
        # Limiteer de totale tijd van een traject
        return trajectory_time <= max_time

    def limit_station_visits(self, station, max_visits):
        # Beperk hoe vaak een station mag worden bezocht
        return self.station_visit_count[station] < max_visits

    def minimize_overlapping_connections(self, current_station, next_station):
        # Vermijd het hergebruiken van dezelfde verbinding
        return (current_station, next_station) not in self.visited_connections

    def prioritize_unvisited_and_short_connections(self, current_station):
        # Sorteer buurstations zodat ongebruikte en korte verbindingen prioriteit hebben
        neighbors = self.rail_network.connection_map[current_station]
        neighbors.sort(key=lambda x: ((current_station, x[0]) not in self.visited_connections, x[1]))
        return neighbors

    def apply_heuristics(self, current_station, trajectory, total_time, max_time, max_visits):
        # Pas alle heuristieken toe om de volgende logische verbinding te kiezen
        for neighbor_station, time in self.prioritize_unvisited_and_short_connections(current_station):
            if self.limit_station_visits(neighbor_station, max_visits) and \
               self.minimize_overlapping_connections(current_station, neighbor_station) and \
               self.limit_max_time_per_trajectory(total_time + time, max_time):
                return neighbor_station, time
        return None

    def calculate_k_score(self, trajectory, total_time):
        # Bereken de K-score voor een traject

        # Totaal aantal verbindingen in het netwerk
        total_connections = len(self.rail_network.connections)

        # Aantal unieke verbindingen bereden
        unique_visited_connections = len(self.visited_connections) // 2
        p = unique_visited_connections / total_connections if total_connections > 0 else 0

        # Formule voor K-score
        T = 1
        K = p * 10000 - (T * 100 + total_time)

        # Maximaliseer K-score op 10.000
        K = min(K, 10000)
        return K

    def generate_trajectories(self, max_trajectories, max_time, max_visits=2):
        # Genereer een set van trajecten met heuristieken
        all_trajectories = []
        sorted_stations = sorted(
            self.rail_network.stations.keys(),

            # Sorteer op aantal verbindingen
            key=lambda s: len(self.rail_network.connection_map[s]),
            reverse=True
        )

        # Kies een subset van stations als startpunten
        start_stations = sorted_stations[:max_trajectories * 2]

        for start_station in start_stations:
            current_station = start_station

            # Begin een nieuw traject
            trajectory = [current_station]
            total_time = 0

            while True:
                next_connection = self.apply_heuristics(
                    current_station, trajectory, total_time, max_time, max_visits
                )
                if next_connection:
                    neighbor_station, time = next_connection
                    trajectory.append(neighbor_station)

                    # Markeer verbinding als bezocht in beide richtingen
                    self.visited_connections.add((current_station, neighbor_station))
                    self.visited_connections.add((neighbor_station, current_station))

                    # Update bezoekfrequentie
                    self.station_visit_count[neighbor_station] += 1
                    total_time += time
                    current_station = neighbor_station
                else:
                    break

            if self.prevent_single_connection_trajectories(trajectory):
                k_score = self.calculate_k_score(trajectory, total_time)
                all_trajectories.append((trajectory, total_time, k_score))

        # Sorteer en selecteer de beste trajecten op basis van K-score
        best_trajectories = sorted(all_trajectories, key=lambda x: x[2], reverse=True)[:max_trajectories]
        return best_trajectories


if __name__ == "__main__":
    rail_network = RailNetwork()

    # Laad de data
    rail_network.load_stations("data/NL/StationsNationaal.csv")
    rail_network.load_connections("data/NL/ConnectiesNationaal.csv")

    # rail_network.load_stations("data/NZ-Holland/StationsHolland.csv")
    # rail_network.load_connections("data/NZ-Holland/ConnectiesHolland.csv")

    heuristics = Heuristics(rail_network)

    max_trajectories = 20
    max_time = 180

    # max_trajectories = 7
    # max_time = 120

    # Genereer en print de beste trajecten
    best_trajectories = heuristics.generate_trajectories(max_trajectories, max_time)
    print("Top 20 Trajectories with Highest K-Scores:")
    for i, (trajectory, time, k_score) in enumerate(best_trajectories, 1):
        print(f"Trajectory {i}: {' -> '.join(trajectory)} (Total Time: {time} minutes, K-Score: {k_score:.2f})")
