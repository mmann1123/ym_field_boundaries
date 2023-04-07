# %%


import shutil
from pathlib import Path

# from .data_original import p
from cultionet.scripts.cultionet import open_config
from cultionet.data.create import create_predict_dataset
from cultionet.utils import model_preprocessing
from cultionet.utils.project_paths import setup_paths

p = Path("/home/ubuntu/training_data")
# p = Path("/home/ubuntu/cultionet/tests/data")
CONFIG = open_config("/home/ubuntu/ym_field_boundaries/4_cultionet_config.yml")
END_YEAR = CONFIG["years"][-1]
REGION = f"{CONFIG['regions'][-1]:06d}"


def get_image_list():
    image_list = []
    for image_vi in CONFIG["image_vis"]:
        vi_path = p / "time_series_vars" / REGION / image_vi
        ts_list = model_preprocessing.get_time_series_list(
            vi_path,
            END_YEAR - 1,
            CONFIG["start_date"],
            CONFIG["end_date"],
            date_format="%Y%j",
        )
        image_list += ts_list

    return image_list


# import sys

# sys.path.append("/")
# sys.path.append("/home/ubuntu/cultionet/")
# import cultionet


def test_predict_dataset():
    ppaths = setup_paths(".", append_ts=True)
    image_list = get_image_list()

    print("image_list ", image_list)
    print("REGION ", REGION)
    print("END_YEAR ", END_YEAR)
    print("process_path ", ppaths.get_process_path("predict"))

    create_predict_dataset(
        image_list=image_list,
        region=REGION,
        year=END_YEAR,
        process_path=ppaths.get_process_path("predict"),
        gain=1e-4,
        offset=0.0,
        # set the ref res to match image resolution
        ref_res=8.983152841195214829e-05,
        resampling="nearest",
        window_size=50,
        padding=5,
        num_workers=2,
        chunksize=100,
    )
    pt_list = list(ppaths.get_process_path("predict").glob("*.pt"))

    assert len(pt_list) > 0, "No .pt files were created."

    # this erases the outputs
    # shutil.rmtree(str(ppaths.get_process_path("predict")))


# creates the .pt files in current directory
test_predict_dataset()

# %%
