import sys
sys.argv.append(["--max-memory", "5G"])

import datetime
import geopandas as gpd
from r5py import TransportNetwork
from r5py import DetailedItinerariesComputer, TransportMode

transport_network = TransportNetwork(
    "Data/OSM/openstreetmap_capnat.pbf",
    [
        "Data/RTC/googletransit.zip"
    ]
)

origin = gpd.GeoDataFrame({"id": [0]},geometry=gpd.GeoSeries(gpd.points_from_xy([-71.15967163926403], [46.88643342800633])), crs="EPSG:4326")
points = gpd.GeoDataFrame({"id": [1]},geometry=gpd.GeoSeries(gpd.points_from_xy([-71.20567619972353], [46.88471757520844])), crs="EPSG:4326")

travel_time_matrix_computer = DetailedItinerariesComputer(
    transport_network,
    origins=origin,
    destinations=points,
    departure=datetime.datetime(2025,3,4,8,30),
    transport_modes=[TransportMode.BUS, TransportMode.WALK]
)

travel_time_matrix = travel_time_matrix_computer.compute_travel_details()

travel_time_matrix["departure_time"] = travel_time_matrix["departure_time"].astype(str)
travel_time_matrix["travel_time"] = travel_time_matrix["travel_time"].astype(str)
travel_time_matrix["wait_time"] = travel_time_matrix["wait_time"].astype(str)

# save to geojson
travel_time_matrix.to_file("itinerary1_bus.geojson", driver="GeoJSON")
