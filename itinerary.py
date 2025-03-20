import sys

sys.argv.append(["--max-memory", "5G"])

import datetime
import os
import geopandas as gpd
from r5py import TransportNetwork, DetailedItinerariesComputer, TransportMode


class CustomItinerary:
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
            "Data/OSM/openstreetmap_capnat.pbf", ["Data/RTC/googletransit.zip"]
        )

    def compute_itinerary(
        self,
        origin_tuple,
        destination_tuple,
        transport_str,
        departure=datetime.datetime.now(),
    ):
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
        origin = gpd.GeoDataFrame(
            {"id": [0]},
            geometry=gpd.GeoSeries(
                gpd.points_from_xy([origin_tuple[0]], [origin_tuple[1]])
            ),
            crs="EPSG:4326",
        )
        destination = gpd.GeoDataFrame(
            {"id": [1]},
            geometry=gpd.GeoSeries(
                gpd.points_from_xy([destination_tuple[0]], [destination_tuple[1]])
            ),
            crs="EPSG:4326",
        )
        transport_modes = self.get_transport_modes(transport_str)

        itinerary_computer = DetailedItinerariesComputer(
            self.transport_network,
            origins=origin,
            destinations=destination,
            departure=departure,
            transport_modes=transport_modes,
        )

        itinerary = itinerary_computer.compute_travel_details()
        one_itinerary = self.get_best_itinerary(itinerary)
        self.save_itinerary(one_itinerary, origin_tuple, destination_tuple)

        return one_itinerary

    def get_best_itinerary(self, df):
        """
        Get the best itinerary from the computed itinerary

        Parameters
        ----------
        df : gpd.GeoDataFrame
            GeoDataFrame containing the itinerary

        Returns
        -------
        gpd.GeoDataFrame
            GeoDataFrame containing the best itinerary
        """
        # Convertir travel_time en secondes pour l'agrégation
        df["travel_time_seconds"] = df["travel_time"].dt.total_seconds()

        # Calculer le temps total de trajet par option
        total_travel_time = df.groupby("option")["travel_time_seconds"].sum()

        # Trouver l'option avec le temps total le plus court
        best_option = total_travel_time.idxmin()

        # Filtrer le GeoDataFrame pour ne garder que les lignes correspondant à cette option
        best_option_df = df[df["option"] == best_option]

        return best_option_df.reset_index(drop=True)

    def save_itinerary(self, itinerary, origin, destination):
        """
        Save the itinerary to a GeoJSON file

        Parameters
        ----------
        itinerary : gpd.GeoDataFrame
            GeoDataFrame containing the itinerary
        origin : tuple
            Tuple containing the origin point (longitude, latitude)
        destination : tuple
            Tuple containing the destination point (longitude, latitude)
        """
        itinerary["departure_time"] = itinerary["departure_time"].astype(str)
        itinerary["travel_time"] = itinerary["travel_time"].astype(str)
        itinerary["wait_time"] = itinerary["wait_time"].astype(str)

        with open("Result/itinerary.geojson", "w+") as f:
            f.write("""var itinerary = {\
"type": "FeatureCollection",\
"name": "itinerary",\
"crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },\
"features": [{ "type": "Feature", "properties": { \
"name": "origin" }, "geometry": { "type": "Point", "coordinates":""")
            f.write(f"""[ {origin[0]}, {origin[1]} ]""")
            f.write(" } },")

            f.write("""{ "type": "Feature", "properties": { \
"name": "destination" }, "geometry": { "type": "Point", "coordinates":""")
            f.write(f"""[ {destination[0]}, {destination[1]} ]""")
            f.write(" } },")

            for i, row in itinerary.iterrows():
                f.write("""{ "type": "Feature", "properties": { """)
                f.write(f'''"from_id": {row["from_id"]}, "to_id": {row["to_id"]}, "option": {row["option"]}, \
"segment": {row["segment"]}, "transport_mode": "{row["transport_mode"]}", "departure_time": \
"{row["departure_time"]}", "distance": {row["distance"]}, "travel_time": "{row["travel_time"]}", \
"wait_time": "{row["wait_time"]}", "route": {('"' + row["route"] + '"') if row["route"] is not None else "null"},''')
                f.write(""" }, "geometry": { "type": "LineString", "coordinates": """)
                line = row["geometry"]
                # Conversion en liste de listes
                coords_list = [list(coord) for coord in line.coords]
                f.write(str(coords_list))
                if i == len(itinerary.index) - 1:
                    f.write(" } } ] }")
                else:
                    f.write(" } },")
        f.close()

    def __del__(self):
        # os.remove("Result/itinerary.geojson")
        pass


if __name__ == "__main__":
    # Define the origin and destination points
    origin = (-71.17019385467583, 46.88585415050622)
    destination = (-71.2777943192087, 46.78035452548721)

    # Define the transport modes
    transport_modes = ["bus"]

    # Compute the itinerary
    itinerary = CustomItinerary()
    best_itinerary = itinerary.compute_itinerary(origin, destination, transport_modes)

    print(best_itinerary)
