'''GPSの速度データを積分してv-t,x-tグラフを出力したい'''

# %% 
from os import name
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

PATH_TO_DATA_DIR : str = "/home/iori/daxue/bache_thesis/20240629_down_Futamata_to_Shinjohara/"
PATH_TO_SOURCE_FILE :str = PATH_TO_DATA_DIR + "gps_distance_omitted_firstzeros.csv"

df = pl.read_csv(PATH_TO_SOURCE_FILE).select(["localtime_datetime","speed","distance/m"])
#%%
local_datetime = np.array(df["localtime_datetime"])
speed = np.array(df["speed"])
distance = np.array(df["distance/m"])
#%%
fig = go.Figure(
    data = [
        go.Scatter(x=local_datetime,y=speed*3.6,name='speed'),
        go.Scatter(x=local_datetime,y=distance/1000,name='distance'),
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
)

fig.show()
offline.plot(fig,filename='run_curve_0629down')
# %%