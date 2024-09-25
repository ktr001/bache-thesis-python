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

PATH_TO_DATA_DIR : str = "/home/iori/daxue/bache_thesis/20240629_down_Futamata_to_Shinjohara/"
PATH_TO_DATA_SOURCE : str = PATH_TO_DATA_DIR +"gps_omitted_firstzeros.csv"
PATH_TO_TARGET_FILE :str = PATH_TO_DATA_DIR + "gps_distance_omitted_firstzeros.csv"
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
add_localtime_timedelta : pl.Expr = (( pl.col("localtime_datetime") - first_localtime).dt.total_milliseconds()/1000 ).alias("localtime_timedelta")
add_GPStime_timedelta : pl.Expr = (( pl.col("GPStime_datetime") - first_GPStime).dt.total_milliseconds()/1000 ).alias("GPStime_timedelta")
# %%
df_raw = df_raw.with_columns(add_localtime_timedelta).with_columns(add_GPStime_timedelta)
# %%
speed_array = np.array(df_raw.get_column("speed") ) # the column 'speed' is already m/s
time_array: np.ndarray = np.array( (df_raw.get_column("localtime_timedelta")))
# %%
distance_array : np.ndarray = np.array([0.0 for i in time_array]) #init
memo:int = 10000
for i in range(len(time_array)):
    if i==0:
        distance_array[i] = 0
    elif i < memo:
        distance_array[i] = integrate.simpson(y = speed_array[0:i+1], x = time_array[0:i+1])
    else:
        distance_array[i] = distance_array[i-memo] + integrate.simpson(y = speed_array[i-memo:i+1], x = time_array[i-memo:i+1])
# %%
local_time_array:np.ndarray = np.array(df_raw["localtime_datetime"].dt.to_string("%H:%M:%S%.f"))

go.Figure(
    data = [
        go.Scatter(x=local_time_array,y=speed_array*3.6,name='speed'),
        go.Scatter(x=local_time_array,y=distance_array/1000,name='distance'),
    ]
).update_layout(
    title='run curve(km/h,km)',
    legend=dict(
        xanchor='left',
        yanchor='bottom',
        x=0.02,
        y=0.9,
        orientation='h',
        )
).show()
# %%
distance_series:pl.Series = pl.Series('distance/m',distance_array)
# %%
df_with_distance = df_raw.with_columns(distance_series)
# %%
df_with_distance.write_csv(PATH_TO_TARGET_FILE)
# %%