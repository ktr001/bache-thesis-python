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

PATH_TO_0630_DATA_DIR : str = "/home/iori/daxue/bache_thesis/20230630_軌道変位データ/"
SOURCE_0630_FILE :str = PATH_TO_0630_DATA_DIR + "TGdata20230630.csv"
PATH_TO_0126_DATA_DIR : str = "/home/iori/daxue/bache_thesis/20240126_軌道変位データ/"
SOURCE_0126_FILE :str = PATH_TO_0126_DATA_DIR + "TGdata20240126.csv"

# convTo_datetime :pl.Expr = pl.col(
#     "localTimeStamp"
#     ).str.to_datetime(
#         format= "%Y/%m/%d %H:%M:%S%.f"
#         )

SOURCE_FILE :str = SOURCE_0630_FILE

df = pl.read_csv(SOURCE_FILE)


#%%