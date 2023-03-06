# %% install randombox
# pip install git+https://github.com/mmann1123/randombox.git
# %%
from randombox import random_box
import glob as glob
import os

os.chdir(
    "/home/mmann1123/extra_space/Dropbox/TZ_field_boundaries/training_data/time_series_vars/"
)
directory_list = os.listdir()
directory_list

# %%
# create random boxes for training and validation

# 2021 data polygon labeled at end of crop season so 2022 (see cultionet docs)
for directory in directory_list:
    geo_path = os.path.join(directory, "evi", "2021091.tif")

    num_points = 5
    size = 1000
    squares_gdf = random_box(
        geo_path,
        num_points,
        size,
        out_path = os.path.join(os.path.dirname(os.getcwd()), 'user_train' )
        name_prefix=directory,
        name_postfix="2022",
        crs="EPSG:3395",
    )

# 2022 data polygon labeled at end of crop season so 2023

for directory in directory_list:
    geo_path = os.path.join(directory, "evi", "2021091.tif")

    num_points = 52
    size = 1000
    squares_gdf = random_box(
        geo_path,
        num_points,
        size,
        out_path = os.path.join(os.path.dirname(os.getcwd()), 'user_train' )
        name_prefix=directory,
        name_postfix="2023",
        crs="EPSG:3395",
    )

# %%
