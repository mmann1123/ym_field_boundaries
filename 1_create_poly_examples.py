# %% install randombox
#!pip install git+https://github.com/mmann1123/randombox.git
# !git clone https://github.com/mmann1123/randombox.git
# !pip install -e randombox
# %%
from randombox import random_box

# %%
import glob as glob
import os

main_path = r"/home/mmann1123/Dropbox/TZ_field_boundaries"  # desktop /home/mmann1123/extra_space/Dropbox/TZ_field_boundaries/
main_path = r"/home/mmann1123/extra_space/Dropbox/TZ_field_boundaries/"
main_path

os.chdir(os.path.join(main_path, "training_data/time_series_vars/"))
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
            out_dir=os.path.join(
                os.path.dirname(os.getcwd()), "user_train_dummy_to avoid overwrite"
            ),
            name_prefix=directory,
            name_postfix=year,
            crs="EPSG:3395",
        )
# ####################################################
# NOTE these must be edited manually to drwaw polygons around fields.


# %%  BREAK POLY AND GRID INTO INDIVIDUAL FILES WITH 6 DIGIT CODES
import geopandas as gpd
from random import randint, seed
import os

main_path = r"/home/mmann1123/Dropbox/TZ_field_boundaries"  # desktop
main_path = r"/home/mmann1123/extra_space/Dropbox/TZ_field_boundaries/"

# read in _poly_ and _grid_ with multiple features each and export aois as individual geopackages
os.chdir(os.path.join(main_path, "training_data/user_train/"))

# get region names
regions = sorted(os.listdir(r"../../raw_images_S2"))
regions


in_path = os.path.join(os.getcwd(), "multi_feature_by_region")
out_path = os.path.join(os.getcwd(), "single_feature_by_id")

os.makedirs(out_path, exist_ok=True)

# %%
zone = 1
# read in _poly_ and _grid_ files, find intersection between individual _grid_ and _poly_, export aois as individual geopackages
for year in ["2022", "2023"]:
    # reset zone counter after each year

    for region in regions:
        try:
            grid = gpd.read_file(os.path.join(in_path, f"{region}_grid_{year}.geojson"))
            poly = gpd.read_file(os.path.join(in_path, f"{region}_poly_{year}.geojson"))
        except:
            continue
        # iterate through each grid geometry and find intersection with poly
        for i, row in grid.iterrows():
            # find intersection
            intersection = gpd.overlay(
                poly,
                gpd.GeoDataFrame(geometry=[row.geometry], crs=grid.crs),
                how="intersection",
                keep_geom_type=False,
            )
            # add required field
            intersection["class"] = 1
            intersection["grid"] = f"{zone:06d}"

            # write to geopackage
            intersection.to_crs("EPSG:4326", inplace=True)

            intersection.to_file(
                os.path.join(out_path, f"{zone:06d}_poly_{year}.gpkg"),
                driver="GPKG",
                layer=f"{zone}_poly_{year}",
            )
            grid_out = gpd.GeoDataFrame(geometry=[row.geometry], crs=grid.crs)
            grid_out["class"] = 1
            grid_out["grid"] = f"{zone:06d}"

            grid_out.to_crs("EPSG:4326", inplace=True)

            grid_out.to_file(
                os.path.join(out_path, f"{zone:06d}_grid_{year}.gpkg"),
                driver="GPKG",
                layer=f"{zone}_grid_{year}",
            )

            zone += 1

# %%  add column called "class" with value 1 to all polygons in each geopackage
# import os
# import geopandas as gpd
# from glob import glob

# # !mkdir /home/ubuntu/training_data/user_train/gpkg
# os.chdir("/home/ubuntu/training_data/user_train")
# for afile in glob("*.geojson"):
#     filename, file_extension = os.path.splitext(afile)
#     gdf = gpd.read_file(afile)
#     gdf["class"] = 1
#     gdf.to_crs("epsg:4326").to_file(f"{filename}.gpkg", driver="GPKG")

# # %%
# import os
# import geopandas as gpd
# from glob import glob

# os.chdir("/home/ubuntu/training_data/user_train")
# for afile in glob("*.geojson"):
#     gdf = gpd.read_file(afile)
#     gdf["class"] = 1
#     gdf.to_file(afile, driver="GeoJSON")
# # %%

# # %%

# import geopandas as gpd
# import fiona

# gpkg = "/home/mmann1123/Downloads/user_train_usa/000001_grid_2022.gpkg"
# layers = fiona.listlayers(gpkg)
# %%
# %%  BREAK POLY AND GRID INTO INDIVIDUAL FILES WITH 6 DIGIT CODES
import geopandas as gpd
from random import randint, seed
import os

main_path = r"/home/mmann1123/Dropbox/TZ_field_boundaries"  # desktop
main_path = r"/home/mmann1123/extra_space/Dropbox/TZ_field_boundaries/"

# read in _poly_ and _grid_ with multiple features each and export aois as individual geopackages
os.chdir(os.path.join(main_path, "training_data/user_train/"))

# get region names
regions = sorted(os.listdir(r"../../raw_images_S2"))
regions


in_path = os.path.join(os.getcwd(), "multi_feature_by_region")
out_path = os.path.join(os.getcwd(), "single_feature_by_id2")

os.makedirs(out_path, exist_ok=True)

# %% NOT WORKING

# read in _poly_ and _grid_ files, find intersection between individual _grid_ and _poly_, export aois as individual geopackages
for year in ["2022"]:
    # reset zone counter after each year
    zone = 1
    for region in regions:
        try:
            # get location of target grid
            target_grid = gpd.read_file(
                os.path.join(in_path, f"{region}_grid_{year}.geojson")
            )
        except:
            continue
        # iterate through each grid geometry and find intersection with poly
        for i, target in target_grid.iterrows():
            for year in ["2022", "2023"]:
                try:
                    grid = gpd.read_file(
                        os.path.join(in_path, f"{region}_grid_{year}.geojson")
                    )
                    poly = gpd.read_file(
                        os.path.join(in_path, f"{region}_poly_{year}.geojson")
                    )
                except:
                    continue
                # find intersection of target with grid and poly and write to file
                poly_intersection = gpd.overlay(
                    poly,
                    gpd.GeoDataFrame(geometry=[target.geometry], crs=grid.crs),
                    how="intersection",
                    keep_geom_type=False,
                )
                # add required field
                poly_intersection["class"] = 1
                poly_intersection["grid"] = f"{zone:06d}"

                poly_intersection.to_crs("EPSG:4326", inplace=True)

                poly_intersection.to_file(
                    os.path.join(out_path, f"{zone:06d}_poly_{year}.gpkg"),
                    driver="GPKG",
                    layer=f"{zone}_poly_{year}",
                )

                grid_out = gpd.GeoDataFrame(geometry=[target.geometry], crs=grid.crs)
                if grid_out.is_empty[0]:
                    grid_out["class"] = 0
                else:
                    grid_out["class"] = 1

                grid_out["grid"] = f"{zone:06d}"

                grid_out.to_crs("EPSG:4326", inplace=True)

                grid_out.to_file(
                    os.path.join(out_path, f"{zone:06d}_grid_{year}.gpkg"),
                    driver="GPKG",
                    layer=f"{zone}_grid_{year}",
                )

                zone += 1
    # %%
