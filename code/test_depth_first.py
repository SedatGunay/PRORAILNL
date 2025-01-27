from depth_first import DepthFirstRailNetwork

def main():
    rail_network = DepthFirstRailNetwork(max_time_limit=180)
    rail_network.load_stations(r"/Users/sedatgunay/Documents/GitHub/PRORAILNL/data/NL/StationsNationaal.csv")
    rail_network.load_connections(r"/Users/sedatgunay/Documents/GitHub/PRORAILNL/data/NL/ConnectiesNationaal.csv")
    
    # Test
    start_station = "Amsterdam Centraal"
    end_station = "Rotterdam Centraal"

    time_limit = 180

    routes = rail_network.find_routes(start_station, end_station, time_limit)
    print(len(routes))


if __name__ == "__main__":
    main()