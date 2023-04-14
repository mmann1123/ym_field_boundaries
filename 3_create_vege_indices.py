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
print('image periods' , image_periods)

grids = glob(r'./training_data/user_train/single_feature_by_id/*grid*.gpkg')
# grids_years = list(set([ int(re.findall(r'\d{4}', grid)[1]) for grid in  grids  ]))
print('grids' , grids)

out_path_tile ='./training_data/time_series_vars'
out_path_mosaic = './mosaic/evi'

os.makedirs(out_path_tile,exist_ok=True)
os.makedirs(out_path_mosaic,exist_ok=True)

 
#%%
for image_period in image_periods:
    print('image period: ',image_period,'---------\n')
    with gw.config.update(sensor='bgrn',ref_crs='EPSG:32736'  ):
        with gw.open([os.path.join(folder, image_period) for folder in image_folders], 
                    mosaic=True ,
                    overlap="max",
                    bounds_by="union",
                    chunks=1024) as ds: 
            evi = ds.gw.evi(scale_factor =1).compute(workers=8 )
            evi2 = evi.gw.match_data(ds,['evi'])
            print('writing: ',os.path.join(out_path_mosaic,image_period))
            evi2.gw.save(
                    os.path.join(out_path_mosaic,image_period), 
                    overwrite=True,
                    num_workers=8 )

    #subset grids list to year (image year + 1 to match end of crop seaon)
    year_grids = [x for x in grids if str(int(re.findall(r'\d{4}', image_period)[0])+1) in x]
        
    for grid in year_grids:
        print('grid: ',grid,'---------\n')

        # clip with ref bounds instead of clip (bug)
        grid2 = gpd.read_file(grid).to_crs('EPSG:32736') 

        # buffer grid by 3m to avoid edge effects
        expand = 8.983152841195215e-05 *0.25
        with gw.config.update(ref_bounds=grid2.buffer(expand).total_bounds.tolist()):
            with gw.open(
                os.path.join(out_path_mosaic,image_period),
                chunks=1024, ) as ds_evi:

                #ds2 = ds_evi.gw.clip(grid2)
                assert ds_evi.compute().shape == (1, 100, 100)
                
                grid_code = re.findall(r'\d{6}', os.path.basename(grid))[0]
                out_dir = os.path.join(out_path_tile,
                                    grid_code,
                                    'evi')
                os.makedirs(out_dir,exist_ok=True)
                print(os.path.join(out_dir,image_period))
                ds_evi.gw.to_raster(os.path.join(out_dir,image_period),overwrite=True)
    
             

# # %% reproject all images 



# import geowombat as gw
# import geopandas as gpd
# import re
# from glob import glob

# os.chdir('/home/mmann1123/extra_space/Dropbox/TZ_field_boundaries/') # desktop
# # os.chdir(r'/home/mmann1123/Dropbox/TZ_field_boundaries/') # laptop


# evi_imgs = glob('./training_data/time_series_vars/*/*/*.tif', recursive=True)
# evi_imgs

# image_folders = list(set([os.path.dirname(x) for x in evi_imgs]))
# image_folders

# image_periods = list(set([os.path.basename(x) for x in evi_imgs]) )
# print('image periods' , image_periods)

 
# grids = glob(r'./training_data/user_train/single_feature_by_id/*grid*.gpkg')
# print('grids' , grids)

# out_path_tile ='./proj/training_data/time_series_vars'
 
# os.makedirs(out_path_tile,exist_ok=True)
 
# #%% reproject image shards

# for evi_img in evi_imgs:
#     with gw.config.update(ref_crs= 'EPSG:32736', ref_res=10 ):
#         with gw.open(evi_img) as ds: 
#             shard_out_path = os.path.join(out_path_tile,'/'.join(evi_img.split('/')[-3:]))
#             os.makedirs(os.path.dirname(shard_out_path),exist_ok=True)
#             ds.gw.to_raster(shard_out_path,
#                     overwrite=True,
#                     num_workers=8 )

# #%% reproject grid poly
# #   WORK ON THIS!!!!!!!!



# for image_period in image_periods:

#     #subset grids list to year 
#     year_grids = [x for x in grids if re.findall(r'\d{4}', image_period)[0] in x]
        
#     for grid in year_grids:
#         print('grid: ',grid,'---------\n')

#         # clip with ref bounds instead of clip (bug)
#         grid2 = gpd.read_file(grid) 
#         with gw.config.update(ref_bounds=grid2.total_bounds.tolist()):
#             with gw.open(
#                 os.path.join(out_path_mosaic,image_period),
#                 chunks=1024, ) as ds_evi:

#                 #ds2 = ds_evi.gw.clip(grid2)
#                 # ds2.gw.imshow(robust=True, ax=ax)
#                 grid_code = re.findall(r'\d{6}', os.path.basename(grid))[0]
#                 out_dir = os.path.join(out_path_tile,
#                                     grid_code,
#                                     'evi')
#                 os.makedirs(out_dir,exist_ok=True)
#                 print(os.path.join(out_dir,image_period))
#                 ds_evi.gw.to_raster(os.path.join(out_dir,image_period),overwrite=True)
    

# %%
