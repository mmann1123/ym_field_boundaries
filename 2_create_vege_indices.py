#%%
import geowombat as gw
from glob import glob
import os
os.chdir('/home/mmann1123/extra_space/Dropbox/TZ_field_boundaries/raw_images_S2')
files = glob('**/**.tif', recursive=True)
 

#%%
for file in files:
    # create directories for evi and tasseled cap
    names = os.path.split(file)
    ! mkdir -p {names[0]}/evi
    ! mkdir -p {names[0]}/red
    ! mkdir -p {names[0]}/green
    ! mkdir -p {names[0]}/blue

    # read in the file and calculate the indices
    with gw.config.update(sensor='bgrn' ):
        with gw.open(file) as ds:

            print(ds)
            # calculate evi
            evi = ds.gw.evi()
            evi.gw.save(
                os.path.join(names[0],'evi',names[1]), num_workers=4 )
            red = ds.sel(band='red')
            red.gw.save(
                os.path.join(names[0],'red',names[1]), num_workers=4, overwrite=True )
            green = ds.sel(band='green')
            green.gw.save(
                os.path.join(names[0],'green',names[1]), num_workers=4, overwrite=True )
            blue = ds.sel(band='blue')
            blue.gw.save(
                os.path.join(names[0],'blue',names[1]), num_workers=4, overwrite=True )
            
            # moved to time_series_vars folder

# %%
