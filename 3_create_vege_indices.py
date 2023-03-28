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

os.chdir('/home/mmann1123/extra_space/Dropbox/TZ_field_boundaries') # desktop
# os.chdir(r'/home/mmann1123/Dropbox/TZ_field_boundaries/') # laptop


evi_imgs = glob('./raw_images_S2/*/*.tif', recursive=True)
evi_imgs

image_folders = list(set([os.path.dirname(x) for x in evi_imgs]))
image_folders

image_periods = list(set([os.path.basename(x) for x in evi_imgs]) )
image_periods

grids = glob(r'./training_data/user_train/single_feature_by_id/*grid*.gpkg')
grids

out_path ='./training_data/time_series_vars'

#%%
import matplotlib.pyplot as plt

for image_period in image_periods:
    with gw.config.update(sensor='bgrn', ):
        with gw.open([os.path.join(folder, image_period) for folder in image_folders], 
                    mosaic=True ,
                    overlap="mean",
                    bounds_by="union",
                    chunks=1024) as ds: 
            evi = ds.gw.evi(scale_factor =1).compute(workers=8 )
            evi2 = evi.gw.match_data(ds,['evi'])
            os.makedirs('./mosaic/evi',exist_ok=True)
            evi2.gw.save(
                    os.path.join('./mosaic/evi',image_period), 
                    overwrite=True,
                    num_workers=8 )

    #subset grids list to year 
    year_grids = [x for x in grids if re.findall(r'\d{4}', image_period)[0] in x]
        
    for grid in year_grids:
        print('grid: ',grid,'---------\n')

        # clip with ref bounds instead of clip (bug)
        grid2 = gpd.read_file(grid) 
        with gw.config.update(ref_bounds=grid2.total_bounds.tolist()):
            with gw.open(
                os.path.join('./mosaic/evi',image_period),
                chunks=1024, ) as ds_evi:

                #ds2 = ds_evi.gw.clip(grid2)
                # ds2.gw.imshow(robust=True, ax=ax)
                grid_code = re.findall(r'\d{6}', os.path.basename(grid))[0]
                out_dir = os.path.join(out_path,
                                    grid_code,
                                    'evi')
                os.makedirs(out_dir,exist_ok=True)
                print(os.path.join(out_dir,image_period))
                ds_evi.gw.to_raster(os.path.join(out_dir,image_period),overwrite=True)
    


# %%
 