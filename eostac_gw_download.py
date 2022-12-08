#%% eostac env on popos 
# downloads and adjusts radiometric difference
!eostac adjust \
    --start-date 2021-03-01 \
    --end-date 2021-06-01 \
    --out-path ./pry_coefficients \
    --geometry ./bounds/bounds_test.geojson \
    --n-samples 50 \
    --freq Y \
    --freq-repeat 10 \
    --workers 10 \
    --threads 2 \
    --resolution 10.0 
#%%    

from eostac.stac_utils import read_df

df = read_df(r'~/extra_space/Dropbox/Tanzania_data/pry_coefficients/000004/sentinel2/scene.info')

# %%
df_slice = df['2021-01-01':'2022-01-01']
df_slice.id.values.tolist()
df_s2a = df.query("id == 's2a'")

#%%

from pathlib import Path
import geowombat as gw
from eostac.stac_utils import read_df
import matplotlib.pyplot as plt


# Read data from grid 00001
brdf_path = Path('/home/mmann1123/extra_space/Dropbox/Tanzania_data/pry_coefficients/000004/sentinel2')
df = read_df(brdf_path / 'scene.info')
df
#%%
# Ensure only existing files are in the DataFrame
df['file_name'] = df.id+'.tif'
df['file_path'] = brdf_path / df.file_name.map(str)
df['file_path_exists'] = df.file_path.apply(lambda x: x.is_file())
# df = df.loc[df.file_path_exists]
df
#%%
# Get the file, time, and band names
file_list = df.file_path.map(str).values.tolist()
time_names = df.date.dt.strftime('%Y-%m-%d').values.tolist()
band_names = ['blue', 'green', 'red', 'nir', 'swir1', 'swir2']

# Plot a single time slice
with gw.open(
    file_list,
    time_names=time_names,
    band_names=band_names,
    overlap='min'   # We use overlap='min' because the nodata values are 32768.
) as src:
    # View RGB of first date
    (
        src
        .isel(time=0)
        .sel(band=['red', 'green', 'blue'])
        .squeeze()
        .transpose('band', 'y', 'x')
        .where(lambda x: x != x.nodatavals[0])
        .gw.imshow(robust=True)
    )
    plt.show()

# Plot the median over time
with gw.open(
    file_list,
    time_names=time_names,
    band_names=band_names,
    overlap='min'   # We use overlap='min' because the nodata values are 32768.
) as src:
    (
        src
        .sel(band=['red', 'green', 'blue'])
        .transpose('time', 'band', 'y', 'x')
        .where(lambda x: x != x.nodatavals[0])
        .median(dim='time', skipna=True)
        .gw.imshow(robust=True)
    )
    plt.show()
# %%
