# %% install randombox
#!pip install git+https://github.com/mmann1123/randombox.git
# !git clone https://github.com/mmann1123/randombox.git
# !pip install -e randombox
# %%
from randombox import random_box
import glob as glob
import os

# %%
os.chdir(
    "/home/mmann1123/extra_space/Dropbox/TZ_field_boundaries/training_data/time_series_vars/"
)
directory_list = os.listdir()
directory_list

# %%
# create random boxes for training and validation

# 2021 data polygon labeled at end of crop season so 2022 (see cultionet docs)
# also 2022 data (labeled 2023)
for year in ["2022", "2023"]:
    for directory in directory_list:
        geo_path = os.path.join(directory, "evi", "2021091.tif")

        num_points = 10
        size = 1000
        squares_gdf = random_box(
            geo_path,
            num_points,
            size,
            out_dir=os.path.join(os.path.dirname(os.getcwd()), "user_train"),
            name_prefix=directory,
            name_postfix=year,
            crs="EPSG:3395",
        )
# %%

# %%
import geopandas as gpd
from random import randint

# %%
# read in _poly_ and _grid_ files, export aois as individual geopackages
os.chdir(
    "/home/mmann1123/extra_space/Dropbox/TZ_field_boundaries/training_data/user_train/"
)
# get region names
regions = os.listdir(
    "/home/mmann1123/extra_space/Dropbox/TZ_field_boundaries/training_data/time_series_vars/"
)

in_path = os.path.join(os.getcwd(), "multi_feature_by_region")
out_path = os.path.join(os.getcwd(), "single_feature_by_id")

# read in _poly_ and _grid_ files, find intersection between individual _grid_ and _poly_, export aois as individual geopackages
for year in ["2022", "2023"]:
    for region in regions:
        grid = gpd.read(os.path.join(in_path, f"{region}_grid_{year}.geojson"))
        poly = gpd.read(os.path.join(in_path, f"{region}_poly_{year}.geojson"))
        # iterate through each grid geometry and find intersection with poly
        for i, row in grid.iterrows():
            # find intersection
            intersection = gpd.overlay(poly, row, how="intersection")
            # write to geopackage
            intersection.to_file(
                os.path.join(out_path, f"{randint(0, 99999):05d}_{year}_{i}.gpkg"),
                driver="GPKG",
                layer="aoi",
            )


# %%
from shapely.geometry import Point

a = Point(0, 0).intersection(Point(0, 1))


# %%
# use gpd.overlay to check intersection between two polygon geodataframes
def check_intersection(gdf1, gdf2):
    """Check if two geodataframes intersect"""
    # check if gdf1 and gdf2 intersect
    if gpd.overlay(gdf1, gdf2).empty:
        return False
    else:
        return True

 