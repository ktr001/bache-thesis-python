# %% 
from os import name
import plotly.graph_objects as go
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
PATH_TO_SOURCE_FILE :str = PATH_TO_DATA_DIR + "gps_distance_omitted_firstzeros_1st1000.csv"

df = pl.read_csv(PATH_TO_SOURCE_FILE).select(["localtime_datetime","speed","distance/m"])
#%%
local_datetime = np.array(df["localtime_datetime"])
speed = np.array(df["speed"])
distance = np.array(df["distance/m"])
#%%
