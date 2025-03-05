import os
import shutil
import geopandas as gpd
import rasterio
from rasterio.merge import merge
import osmnx as ox
import pandas as pd

# 1. Téléchargement des données OpenStreetMap
# ox.config(log_console=True)
# quebec_graph = ox.graph_from_place("Capitale-Nationale, Québec, Canada", network_type="all")
# ox.save_graphml(quebec_graph, filepath="Data/OSM/openstreetmap_capnat.graphml")

# # 2. Chargement et découpage du polygone de la ville de Québec
# villeqc = gpd.read_file("Data/VilledeQuebec.shp")
# villeqc = villeqc.to_crs(epsg=4326)
# villeqc_buffer = villeqc.buffer(5000)
# bbox = villeqc_buffer.total_bounds

# # Découpage du graphe OSM pour la ville de Québec
# quebec_graph = ox.truncate.truncate_graph_bbox(quebec_graph, bbox[1], bbox[3], bbox[0], bbox[2])
# ox.save_graphml(quebec_graph, filepath="Data/OSM/openstreetmap_qc.graphml")

# 3. Construction du GeoTIFF pour l’élévation
grid_folder = "Data/MNT"

# Fusion des rasters
# raster_files = [os.path.join(grid_folder, f) for f in os.listdir(grid_folder) if f.endswith(".tif")]
# rasters = [rasterio.open(r) for r in raster_files]
# mosaic, transform = merge(rasters)

# with rasterio.open("Data/Elevation.tif", "w", driver="GTiff", 
#                    height=mosaic.shape[1], width=mosaic.shape[2],
#                    count=1, dtype=mosaic.dtype, crs="EPSG:4326", transform=transform) as dst:
#     dst.write(mosaic, 1)

# # Nettoyage des fichiers temporaires
# shutil.rmtree(grid_folder)