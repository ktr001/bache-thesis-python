# %% 
from os import name
import math
from time import localtime
from datetime import datetime,date,time,timedelta

import plotly.graph_objects as go
import numpy as np
import polars as pl
import numpy.typing as npt
from scipy import integrate

from pathlib import Path
import pprint
CURRENT_DIR = Path.cwd()
pprint.pprint(f'__name__ = {__name__}')
pprint.pprint(__name__ == '__main__')
pprint.pprint(CURRENT_DIR)

PATH_TO_DATA_SOURCE_DIR : str = "/home/iori/daxue/bache_thesis/20240629_down_Futamata_to_Shinjohara/"
PATH_TO_DATA_SOURCE : str = PATH_TO_DATA_SOURCE_DIR +"gps_omitted_firstzeros_1st1000.csv"
# %%

df_raw  = pl.read_csv(PATH_TO_DATA_SOURCE)

add_localtime_datetime :pl.Expr = pl.col(
    "localTimeStamp"
    ).str.to_datetime(
        format= "%Y/%m/%d %H:%M:%S%.f"
        ).alias("localtime_datetime")
add_GPStime_datetime :pl.Expr = pl.col(
    "GPStimeStamp"
    ).str.to_datetime(
        format= "%Y/%m/%d %H:%M:%S%.f"
        ).alias("GPStime_datetime")


# %%
df_raw = df_raw.with_columns(add_localtime_datetime).with_columns(add_GPStime_datetime).drop(["localTimeStamp","GPStimeStamp"])
# %%
first_localtime : datetime = df_raw["localtime_datetime"][0]
first_GPStime : datetime = df_raw["GPStime_datetime"][0]
add_localtime_timedelta : pl.Expr = ( pl.col("localtime_datetime") - first_localtime).alias("localtime_timedelta")
add_GPStime_timedelta : pl.Expr = ( pl.col("GPStime_datetime") - first_GPStime).alias("GPStime_timedelta")
# %%
df_raw = df_raw.with_columns(add_localtime_timedelta).with_columns(add_GPStime_timedelta)
# %%
df_speed = np.array(df_raw.get_column("speed"))
df_time = np.array(df_raw.get_column("localtime_timedelta"))
# %%
