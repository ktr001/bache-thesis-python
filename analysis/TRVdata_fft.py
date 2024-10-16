'''
python/MatLabによりリサンプリングしたファイルの結果を比較する。また、それぞれにfft/PSDを計算し、比較する。
'''
#%%

import plotly.graph_objects as go
from plotly import offline
import numpy as np
import numpy.typing as npt
import scipy.signal
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
# PATH_TO_0126_DATA_DIR : str = "/home/iori/daxue/bache_thesis/20240126_軌道変位データ/"
SOURCE_PYTHON_FILE :str = PATH_TO_0630_DATA_DIR + "TGdata20230630_resampled.csv"
SOURCE_MATLAB_FILE :str = PATH_TO_0630_DATA_DIR + "TGdata_resampled_byMatLab_relabeled.csv"
# %%
#  [x] 比較用波形データ読み込み
df_compare_timedata_PY: pl.DataFrame = pl.read_csv(SOURCE_PYTHON_FILE).rename(lambda column_name: column_name + '_py')
df_compare_timedata_MAT: pl.DataFrame = pl.read_csv(SOURCE_MATLAB_FILE).with_columns(pl.col('キロ程(meter)') - 114.5 ).rename(lambda column_name: column_name + '_mat').drop('_mat')
df_compare_timedata = pl.concat([df_compare_timedata_PY,df_compare_timedata_MAT],how = "horizontal")
# %%
# [ ] 波形データでの比較

# %%
# [ ] 平面性、水準のみ読み込み
df_twist_cross = pl.read_csv(SOURCE_PYTHON_FILE).select(['キロ程(meter)','平面性(生波形)','水準(生波形)'])
# [ ] PSDの算出
# [ ] noverlap の 大きさを決める(chatGPT?)
[f_twist,Pxx_twist] =  scipy.signal.welch(
    df_twist_cross['平面性(生波形)'],
    1/(0.25),
    "hamming",
)
[f_cross,Pxx_cross] =  scipy.signal.welch(
    df_twist_cross['水準(生波形)'],
    1/(0.25),
    "hamming",
)

go.Figure(
    [
        go.Scatter(x=f_twist,y=Pxx_twist,name='twist'),
        go.Scatter(x=f_cross,y=Pxx_cross,name='cross-section')
     ]
    ).update_yaxes(type = 'log').update_layout(
    title='PSD calculated by python (twist,cross)',
    legend=dict(
        xanchor='left',
        yanchor='bottom',
        x=0.02,
        y=0.9,
        orientation='h',
        )
).show()

# %%
if __name__ == '__main__':
    pass
    # offline.plot(figure_or_data = fig_wavelength_analysis, filename = PATH_TO_0630_DATA_DIR+'fig_wavelength_analysis_for1st1000data.html')
    # offline.plot(figure_or_data = fig_freq_analysis, filename = PATH_TO_0630_DATA_DIR+'fig_freq_analysis_for1st1000data.html' )

    # offline.plot(figure_or_data = fig_wavelength_analysis, filename = PATH_TO_0630_DATA_DIR+'fig_wavelength_analysis.html')
    # offline.plot(figure_or_data = fig_freq_analysis, filename = PATH_TO_0630_DATA_DIR+'fig_freq_analysis.html' )
    # %%