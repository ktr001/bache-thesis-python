'''ドクター東海のデータ(TG***.csv)の"20K334M"みたいな表記をfloatに変換'''

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
OUTPUT_0630_FILE :str = PATH_TO_0630_DATA_DIR + "TGdata20230630_converted.csv"
PATH_TO_0126_DATA_DIR : str = "/home/iori/daxue/bache_thesis/20240126_軌道変位データ/"
SOURCE_0126_FILE :str = PATH_TO_0126_DATA_DIR + "TGdata20240126.csv"
OUTPUT_0126_FILE :str = PATH_TO_0126_DATA_DIR + "TGdata20240126_converted.csv"

# convTo_datetime :pl.Expr = pl.col(
#     "localTimeStamp"
#     ).str.to_datetime(
#         format= "%Y/%m/%d %H:%M:%S%.f"
#         )

SOURCE_FILE :str = SOURCE_0126_FILE
OUTPUT_FILE :str = OUTPUT_0126_FILE

df = pl.read_csv(SOURCE_FILE)

#%%
conv_K:pl.Expr = ( pl.col("キロ程")
                  .str.extract(r"(\d+(?:\.\d+)?)K", 1)
                  .cast(pl.Float64)
                   .fill_null(0) * 1000 ).alias("KM_to_M")

conv_M:pl.Expr = ( pl.col("キロ程")
     .str.extract(r"(\d+(?:\.\d+)?)M", 1)  # 'M' の前の数値を抽出
     .cast(pl.Float64)
     .fill_null(0)  # 欠損値を0に置換
    ).alias("M_to_meter")

#%%
target_col :str = 'キロ程(meter)'
cols :list = [col for col in df.columns if col != target_col]
cols.insert(0,target_col)
#%%

df = df.with_columns((conv_K + conv_M).alias("キロ程(meter)")).select(cols).drop("キロ程")
#%%
df.write_csv(OUTPUT_FILE)
# %%
