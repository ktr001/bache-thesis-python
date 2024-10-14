#%%
from os import name
import datetime
import plotly.graph_objects as go
from plotly import offline
import numpy as np
import numpy.typing as npt
from bache_thesis_python import fft, resample
import polars as pl
from pathlib import Path
import pprint


CURRENT_DIR = Path.cwd()
pprint.pprint(f'__name__ = {__name__}')
pprint.pprint(f'__name__ == "__main__" = {__name__ == "__main__"}')
pprint.pprint(CURRENT_DIR)

#%%

PATH_TO_0630_DATA_DIR : str = "/home/iori/daxue/bache_thesis/20230630_軌道変位データ/"
SOURCE_0630_FILE :str = PATH_TO_0630_DATA_DIR + "TGdata20230630_converted.csv"
# PATH_TO_0126_DATA_DIR : str = "/home/iori/daxue/bache_thesis/20240126_軌道変位データ/"
# SOURCE_0126_FILE :str = PATH_TO_0126_DATA_DIR + "TGdata20240126_converted.csv"
OUTPUT_0630_FILE:str = PATH_TO_0630_DATA_DIR + "TGdata20230630_resampled.csv"
#%%
F_BASE:float = 1/(0.25) # 元データのfreq = 4(cycle/m)
F_TRANS:float = 8*F_BASE # UP sampling後の周波数 
F_FOR_FFT:float = F_BASE # FFT用の周波数 
#%%
df_source_data = pl.read_csv(SOURCE_0630_FILE).with_columns(pl.col('キロ程(meter)') - 114.5 ) # source data 読み込み,キロ程が114.5Mから始まるので0Mにオフセット
df_resampled_data_tmp : pl.DataFrame = resample(
    df_source_data,
    'キロ程(meter)',
    ['平面性(生波形)','水準(生波形)','10m弦高低(右)(狂い量)','10m弦高低(左)(狂い量)','10m弦通り(右)(生波形)','10m弦通り(左)(生波形)','軌間(生波形)'],
    F_BASE,
    F_TRANS,
    'UP',
)
#%%
df_resampled_data = resample(
    df_resampled_data_tmp,
    'キロ程(meter)',
    ['平面性(生波形)','水準(生波形)','10m弦高低(右)(狂い量)','10m弦高低(左)(狂い量)','10m弦通り(右)(生波形)','10m弦通り(左)(生波形)','軌間(生波形)'],
    F_TRANS,
    F_BASE,
    'DOWN',
)
#%% 
#  [ ] 等間隔サンプリングからのズレの確認
df_compare = pl.DataFrame(
    [
        pl.Series(
            np.array([
                i*(0.25) for i in range(df_resampled_data.height)
                ]
            )
        ).alias('uniform_キロ程'),
        df_resampled_data['キロ程(meter)'].alias('resampled_キロ程'),
    ]

)
#%%
df_compare = df_compare.with_columns(
    (pl.col('uniform_キロ程') - pl.col('resampled_キロ程')).alias('diff')
)
df_compare.describe()
#%%
df_resampled_data.write_csv(OUTPUT_0630_FILE)
#%%