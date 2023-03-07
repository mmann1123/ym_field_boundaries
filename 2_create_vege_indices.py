#%%
import geowombat as gw
from glob import glob
import os
os.chdir('/home/mmann1123/extra_space/Dropbox/TZ_field_boundaries/training_data/raw_images_S2')
files = glob('**/**.tif', recursive=True)

#%%
! pwd

#%%
for file in files:
    # create directories for evi and tasseled cap
    names = os.path.split(file)
    ! mkdir -p {names[0]}/evi

    # read in the file and calculate the indices
    with gw.config.update(sensor='bgrn' ):
        with gw.open(file) as ds:

            print(ds)
            # calculate evi
            evi = ds.gw.evi()
            evi.gw.save(
            os.path.join(names[0],'evi',names[1]), num_workers=4 )
            # moved to time_series_vars folder

# %%