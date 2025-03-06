import sys
sys.argv.append(["--max-memory", "5G"])

import datetime
import os
import geopandas as gpd
from r5py import TransportNetwork, DetailedItinerariesComputer, TransportMode

class CustomItinerary():
    def __init__(self):
        self.set_network()

    def get_transport_modes(self, transport_string):
        """
        Convert a list of transport modes as strings to a list of TransportMode objects
        
        Parameters
        ----------
        transport_string : list of str
            List of transport modes as strings (e.g. ["bus", "walk", "bike", "car"])
        
        Returns
        -------
        list of TransportMode
            List of transport modes as TransportMode objects
        """
        transport_modes = []
        
        for t in transport_string:
            if t == "bus":
                transport_modes.append(TransportMode.BUS)
            elif t == "walk":
                transport_modes.append(TransportMode.WALK)
            elif t == "bike":
                transport_modes.append(TransportMode.BICYCLE)
            elif t == "car":
                transport_modes.append(TransportMode.CAR)
            else:
                raise ValueError(f"Invalid transport mode: {t}")
        
        return transport_modes

    def set_network(self):
        self.transport_network = TransportNetwork(
            "Data/OSM/openstreetmap_capnat.pbf",
            [
                "Data/RTC/googletransit.zip"
            ]
        )

    def compute_itinerary(self, origin_tuple, destination_tuple, transport_str, departure = datetime.datetime.now()):
        """
        Compute the itinerary between two points
        
        Parameters
        ----------
        origin : tuple
            Tuple containing the origin point (longitude, latitude)
        destination : tuple
            Tuple containing the destination point (longitude, latitude)
        transport_str : list of str
            List of transport modes as strings (e.g. ["bus", "walk", "bike", "car"])
        departure : datetime.datetime
            Departure time, default is the current time

        Returns
        -------
        gpd.GeoDataFrame
            GeoDataFrame containing the itinerary
        """
        origin = gpd.GeoDataFrame({"id": [0]},geometry=gpd.GeoSeries(gpd.points_from_xy([origin_tuple[0]], [origin_tuple[1]])), crs="EPSG:4326")
        destination = gpd.GeoDataFrame({"id": [1]},geometry=gpd.GeoSeries(gpd.points_from_xy([destination_tuple[0]], [destination_tuple[1]])), crs="EPSG:4326")
        transport_modes = self.get_transport_modes(transport_str)
        
        itinerary_computer = DetailedItinerariesComputer(
            self.transport_network,
            origins=origin,
            destinations=destination,
            departure=departure,
            transport_modes=transport_modes
        )

        itinerary = itinerary_computer.compute_travel_details()
        itinerary["departure_time"] = itinerary["departure_time"].astype(str)
        itinerary["travel_time"] = itinerary["travel_time"].astype(str)
        itinerary["wait_time"] = itinerary["wait_time"].astype

        itinerary.to_file("Result/itinerary.geojson", driver="GeoJSON")

        return itinerary

    def __del__(self):
        os.remove("Result/itinerary.geojson")

