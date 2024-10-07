'''BPF後の振動データを時間積分後のgpsデータと照らし合わせて、振動データにキロ程を付けたい'''

# %% 
from os import name
import datetime
import plotly.graph_objects as go
from plotly import offline
import numpy as np
import polars as pl

from pathlib import Path
import pprint
CURRENT_DIR = Path.cwd()
pprint.pprint(f'__name__ = {__name__}')
pprint.pprint(f'__name__ == "__main__" = {__name__ == "__main__"}')
pprint.pprint(CURRENT_DIR)

#%%

# [ ] 積分エラー？ gps data の積分で求めた距離(41K150.291M)とドクター東海のデータでの距離(データのラストが68K013.054M,天竜二俣が26K250M => 41K763.054M)が違う

PATH_TO_DATA_DIR : str = "/home/iori/daxue/bache_thesis/20240629_down_Futamata_to_Shinjohara/"
SOURCE_FILE :str = PATH_TO_DATA_DIR + "ang_vel_0629_BPF_omitted_firstzeros.csv"
TIME_DISTANCE_DATA_FILE : str = PATH_TO_DATA_DIR + "gps_distance_omitted_firstzeros.csv"
OUTPUT_FILE : str = PATH_TO_DATA_DIR + "ang_vel_0629_BPF_with_distance_omitted_firstzeros.csv"


# convTo_datetime :pl.Expr = pl.col(
#     "localTimeStamp"
#     ).str.to_datetime(
#         format= "%Y/%m/%d %H:%M:%S%.f"
#         )

df_timedistance:pl.DataFrame = pl.read_csv(TIME_DISTANCE_DATA_FILE).select(["localtime_datetime","speed","distance/m"])
df_timedistance = df_timedistance.rename({'localtime_datetime':'localTimeStamp'}) # rename: alias使わなくても型変換はできるようだ（下記）

df_angvelo : pl.DataFrame = pl.read_csv(SOURCE_FILE)

#%%
df_timedistance = df_timedistance.select(
    [
        pl.col('localTimeStamp').str.to_datetime(
            
        ),
        "speed",
        "distance/m",
    ]
)

df_angvelo = df_angvelo.select( ## Datetime型はTime型とDate型 を datetime.combine()メソッドで結合 .dt.combine()
    [
        pl.date(2023,6,29).dt.combine(
            pl.col('localTimeStamp').str.strptime(
                pl.Time,
                "%H:%M:%S%.f",
            )
        ).alias('localTimeStamp'),
        'x',
        'y',
        'z',
    ]
)
# %%
