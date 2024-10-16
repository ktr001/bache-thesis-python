'''
pythonによりリサンプリングした上でfft.
'''
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

# SOURCE_0630_FILE :str= PATH_TO_0630_DATA_DIR + "TGdata_freqtestdata_1st1000.csv"

# %%
# t = np.array([0.001*(2**i) for i in range(100)])
# t = np.array([0.1*(i) for i in range(1000)])
# wave = np.sin(2*np.pi*t) + 0.5*np.sin(2*0.5*np.pi*t)
# #%%
# graph_fft(raw_data=wave)
# # %%
# result_data:dict[str,npt.NDArray] = fft.calc_amp(wave,10)['result_half']
# df_fft_result : pl.DataFrame = pl.DataFrame(result_data).with_columns( (pl.col('freq')**(-1)).alias('wave_length') )
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
#%%
pl.write_csv()
#%%

df_twist_fft_result:pl.DataFrame =pl.DataFrame(
     fft.calc_amp(np.array(df_resampled_data['平面性(生波形)']),F_FOR_FFT)['result_half']  
             ).with_columns( 
                 (pl.col('freq')**(-1)
                  ).alias('wave_length')
                    ) ## twistについてfft =>逆数取って波長求める

df_crosssection_fft_result:pl.DataFrame = pl.DataFrame(
    fft.calc_amp(
        np.array(
            df_resampled_data['水準(生波形)']
        ),
        fs=F_FOR_FFT,
    )['result_half']
).with_columns(
    (pl.col('freq')**(-1)).alias('wave_length')
)

df_longitudinal_R_fft_result:pl.DataFrame = pl.DataFrame(
    fft.calc_amp(
        np.array(
            df_resampled_data['10m弦高低(右)(狂い量)']
        ),
        fs=F_FOR_FFT,
    )['result_half'],
).with_columns(
    (pl.col('freq')**(-1)).alias('wave_length')
)

df_longitudinal_L_fft_result:pl.DataFrame = pl.DataFrame(
    fft.calc_amp(
        np.array(
            df_resampled_data['10m弦高低(左)(狂い量)']
        ),
        fs=F_FOR_FFT,
    )['result_half'],
).with_columns(
    (pl.col('freq')**(-1)).alias('wave_length')
)

df_alignment_R_fft_result:pl.DataFrame = pl.DataFrame(
    fft.calc_amp(
        np.array(
            df_resampled_data['10m弦通り(右)(生波形)']
        ),
        fs=F_FOR_FFT,
    )['result_half'],
).with_columns(
    (pl.col('freq')**(-1)).alias('wave_length')
)

df_alignment_L_fft_result:pl.DataFrame = pl.DataFrame(
    fft.calc_amp(
        np.array(
            df_resampled_data['10m弦通り(左)(生波形)']
        ),
        fs=F_FOR_FFT,
    )['result_half'],
).with_columns(
    (pl.col('freq')**(-1)).alias('wave_length')
)

df_gauge_fft_result:pl.DataFrame = pl.DataFrame(
    fft.calc_amp(
        np.array(
            df_resampled_data['軌間(生波形)']
        ),
        fs=F_FOR_FFT,
    )['result_half']
).with_columns(
    (pl.col('freq')**(-1)).alias('wave_length')
)
#%%
# データ数多い→まずwavelength < 50m くらいのものに絞る → ampの大きさに従ってfilter
# df_twist_fft_result = df_twist_fft_result.filter(pl.col('amp') > df_twist_fft_result.describe()['amp'][7]*500 )
# df_twist_fft_result = df_twist_fft_result.filter(pl.col('freq') < 0.2)
# df_twist_fft_result = df_twist_fft_result.filter(pl.col('wave_length') < 50 )

#%%
fig_wavelength_analysis: go.Figure = (
    go.Figure(
        data = [
            go.Scatter(x = df_gauge_fft_result['wave_length'], y = df_gauge_fft_result['amp'],name='Gauge'), 
            go.Scatter(x = df_alignment_R_fft_result['wave_length'], y = df_alignment_R_fft_result['amp'],name='Alignment(R)'), 
            go.Scatter(x = df_alignment_L_fft_result['wave_length'], y = df_alignment_L_fft_result['amp'],name='Alignment(L)'),
            go.Scatter(x = df_longitudinal_R_fft_result['wave_length'], y = df_longitudinal_R_fft_result['amp'],name='Longitudinal(R)'),
            go.Scatter(x = df_longitudinal_L_fft_result['wave_length'], y = df_longitudinal_L_fft_result['amp'],name='Longitudinal(L)'),
            go.Scatter(x = df_crosssection_fft_result['wave_length'], y = df_crosssection_fft_result['amp'],name='Cross Level'),
            go.Scatter(x = df_twist_fft_result['wave_length'], y = df_twist_fft_result['amp'],name='Twist'),
        ]
    ).update_layout(
        xaxis = dict(title = 'wave length(m)'),
        yaxis = dict(title = 'amplitude'),
        # title ='wavelength analysis of TRV data 0630 for 1st 1000rows ',
        title ='wavelength analysis of TRV data 0630',
        legend=dict(
            xanchor='left',
            yanchor='bottom',
            x=0.02,
            y=0.9,
            orientation='h',
            ),
        )
)

# %%
fig_freq_analysis = (
    go.Figure(
        data = [
            go.Scatter(x = df_gauge_fft_result['freq'], y = df_gauge_fft_result['amp'],name='Gauge'), 
            go.Scatter(x = df_alignment_R_fft_result['freq'], y = df_alignment_R_fft_result['amp'],name='Alignment(R)'), 
            go.Scatter(x = df_alignment_L_fft_result['freq'], y = df_alignment_L_fft_result['amp'],name='Alignment(L)'),
            go.Scatter(x = df_longitudinal_R_fft_result['freq'], y = df_longitudinal_R_fft_result['amp'],name='Longitudinal(R)'),
            go.Scatter(x = df_longitudinal_L_fft_result['freq'], y = df_longitudinal_L_fft_result['amp'],name='Longitudinal(L)'),
            go.Scatter(x = df_crosssection_fft_result['freq'], y = df_crosssection_fft_result['amp'],name='Cross Level'),
            go.Scatter(x = df_twist_fft_result['freq'], y = df_twist_fft_result['amp'],name='Twist'),
        ]
    ).update_layout(
        xaxis = dict(title = 'frequency(1/m)'),
        yaxis = dict(title = 'amplitude'),
        # title ='frequency analysis of TRV data 0630 for 1st 1000rows ',
        title ='frequency analysis of TRV data 0630',
        legend=dict(
            xanchor='left',
            yanchor='bottom',
            x=0.02,
            y=0.9,
            orientation='h',
            ),
        )
)
#%%
fig_wavelength_analysis.show()
fig_freq_analysis.show()
# %%
if __name__ == '__main__':
    pass
    # offline.plot(figure_or_data = fig_wavelength_analysis, filename = PATH_TO_0630_DATA_DIR+'fig_wavelength_analysis_for1st1000data.html')
    # offline.plot(figure_or_data = fig_freq_analysis, filename = PATH_TO_0630_DATA_DIR+'fig_freq_analysis_for1st1000data.html' )

    # offline.plot(figure_or_data = fig_wavelength_analysis, filename = PATH_TO_0630_DATA_DIR+'fig_wavelength_analysis.html')
    # offline.plot(figure_or_data = fig_freq_analysis, filename = PATH_TO_0630_DATA_DIR+'fig_freq_analysis.html' )
    # %%