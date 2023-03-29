# %%

# not used


# import geowombat as gw
# from glob import glob
# import os
# import matplotlib.pyplot as plt

# #%%
# os.chdir(r"/home/mmann1123/extra_space/Dropbox/Tanzania_data/")
# paths = sorted(glob("gee_tiles/*.tif"))
# paths


# # %%
# files = [os.path.basename(tile) for tile in paths]
# files
# # %% Mosaic monthly shards

# for year in range(2021, 2023)[0:1]:
#     for month in range(1, 13)[0:1]:
#         print(year, month)
#         filenames = list(
#             filter(lambda x: f"S2_SR_{year}_{str(month).zfill(2)}" in x, paths)
#         )

#         fig, ax = plt.subplots(dpi=200)
#         with gw.config.update(bigtiff="YES"):
#             with gw.open(
#                 filenames,
#                 band_names=["B2", "B3", "B4", "B8"],
#                 mosaic=True,
#                 overlap="mean",
#                 bounds_by="union",
#                 nodata=0,
#             ) as src:
#                 # src.sel(band="B2").plot.imshow(robust=True, ax=ax)
#                 # plt.tight_layout(pad=1)
#                 src.gw.to_raster(
#                     filename=rf"./gee_mosaics/S2_SR_{year}_{month}.tif",
#                     n_workers=0,
#                     n_threads=2,
#                     compress="lzw",
#                 )

# # %%
