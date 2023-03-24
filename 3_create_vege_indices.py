#%%
import geowombat as gw
from glob import glob
import os
# os.chdir('/home/mmann1123/extra_space/Dropbox/TZ_field_boundaries/raw_images_S2') # desktop
os.chdir(r'/home/mmann1123/Dropbox/TZ_field_boundaries/raw_images_S2') # laptop
files = glob('**/**.tif', recursive=True)
files

#%%
for file in files:
    # create directories for evi and tasseled cap
    names = os.path.split(file)
    ! mkdir -p {names[0]}/evi
    # ! mkdir -p {names[0]}/red
    # ! mkdir -p {names[0]}/green
    # ! mkdir -p {names[0]}/blue

    # read in the file and calculate the indices
    with gw.config.update(sensor='bgrn' ):
        with gw.open(file) as ds:

            print(ds)
            # calculate evi
            evi = ds.gw.evi()
            evi.gw.save(
                os.path.join(names[0],'evi',names[1]), num_workers=4 )
            # red = ds.sel(band='red')
            # red.gw.save(
            #     os.path.join(names[0],'red',names[1]), num_workers=4, overwrite=True )
            # green = ds.sel(band='green')
            # green.gw.save(
            #     os.path.join(names[0],'green',names[1]), num_workers=4, overwrite=True )
            # blue = ds.sel(band='blue')
            # blue.gw.save(
            #     os.path.join(names[0],'blue',names[1]), num_workers=4, overwrite=True )
            
            # moved to time_series_vars folder

# %% Create image chips for each grid polygon 
from glob import glob
os.chdir('/home/mmann1123/extra_space/Dropbox/TZ_field_boundaries/training_data/time_series_vars')
evi_imgs=glob('./*/evi/*.tif', recursive=True)
evi_imgs

image_folders = list(set([os.path.dirname(x) for x in evi_imgs]))
image_folders

image_names = list(set([os.path.basename(x) for x in evi_imgs]) )
image_names

grids = glob(r'../user_train/single_feature_by_id/*grid*.gpkg')
grids

#%%
import geowombat as gw
import geopandas as gpd
for image_period in image_names[0:1]:

    with gw.open([os.path.join(folder, image_period) for folder in image_folders], 
                 mosaic=True) as ds:
        for grid in grids:
            grid2 =gpd.read_file(grid).to_crs('EPSG:4326')
            ds = ds.gw.clip(grid2)
            ds
# %%
