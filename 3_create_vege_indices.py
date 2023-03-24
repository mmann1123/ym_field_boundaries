#%%
import geowombat as gw
from glob import glob
import os
# os.chdir('/home/mmann1123/extra_space/Dropbox/TZ_field_boundaries/raw_images_S2') # desktop
os.chdir(r'/home/mmann1123/Dropbox/TZ_field_boundaries/') # laptop
files = glob('raw_images_S2/**/**.tif', recursive=True)
files

#%% CREATE INDICIES FOR ANALYSIS
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

import geowombat as gw
import geopandas as gpd
import re
from glob import glob

# os.chdir('/home/mmann1123/extra_space/Dropbox/TZ_field_boundaries/raw_images_S2') # desktop
os.chdir(r'/home/mmann1123/Dropbox/TZ_field_boundaries/') # laptop


evi_imgs = glob('./training_data/time_series_vars/*/evi/*.tif', recursive=True)
evi_imgs

image_folders = list(set([os.path.dirname(x) for x in evi_imgs]))
image_folders

image_names = list(set([os.path.basename(x) for x in evi_imgs]) )
image_names

grids = glob(r'./training_data/user_train/single_feature_by_id/*grid*.gpkg')
grids



#%%

for image_period in image_names[0:1]:

    with gw.open([os.path.join(folder, image_period) for folder in image_folders], 
                    mosaic=True,chunks=64) as ds: #
        for grid in grids:
            print('grid: ',grid)
            grid2 = gpd.read_file(grid) 
            ds2 = ds.gw.clip(grid2)
            grid_code = re.findall(r'\d{6}', os.path.basename(grid))[-1]
            out_dir = os.path.join('./training_data/time_series_vars',
                                   grid_code,
                                   'evi')
            os.makedirs(out_dir,exist_ok=True)
            print(os.path.join(out_dir,image_period))
            ds2.gw.to_raster(os.path.join(out_dir,image_period),overwrite=True)
            

# %%
 