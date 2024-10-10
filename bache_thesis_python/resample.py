## reference : https://qiita.com/Qooniee/items/7dde8602ca41a1fd5790

from pathlib import Path
import pprint
CURRENT_DIR = Path.cwd()
pprint.pprint(f'__name__ = {__name__}')
pprint.pprint(f'__name__ == "__main__" = {__name__ == "__main__"}')
pprint.pprint(f'CURRENT_DIR={CURRENT_DIR},\tFILENAME={__file__}')

import numpy as np
import numpy.typing as npt
import polars as pl
from pprint import pprint


def butterlowpass(x, fpass, fstop, gpass, gstop, fs, dt, graphCheckflag=False, labelname='Signal[-]'):
    '''
    x: 入力データ
    fpass: 通過域端周波数[Hz]
    fstop: 阻止域端周波数[Hz]
    gpass: 通過域最大損失量[dB]
    gstop: 阻止域最大損失量[dB]
    fs: サンプリング周波数[Hz]
    dt: サンプリング間隔[s]
    checkflag: グラフ生成ON/OFF
    labelname: 信号ラベル名
    
    :return:　フィルター後データ
    バターワースを用いたローパスフィルタ
    filtfilt関数により位相ずれを防ぐ
    (順方向と逆方向からフィルタをかけて位相遅れを相殺)
    '''
    from scipy import signal
    # import matplotlib.pyplot as plt
    from plotly import graph_objects as go
    # [x] matplotlib を plotlyに
    import numpy as np

    print('Applying filter against: {0}...'.format(labelname))
    fn = 1 / (2 * dt)
    Wp = fpass / fn
    Ws = fstop / fn
    N, Wn = signal.buttord(Wp, Ws, gpass, gstop)
    b1, a1 = signal.butter(N, Wn, "low")
    y = signal.filtfilt(b1, a1, x)
    print(y)
    
    if graphCheckflag == True:
        time = np.arange(x.__len__()) * dt
        
        fig_data = [
            go.Scatter(x = time, y = x, name = 'Raw signal'),
            go.Scatter(x = time, y = y, name = 'Filtered signal')
            ]
        fig = go.Figure(data = fig_data).update_layout(
            xaxis = dict(title = 'Time(s) or length(m)'),
            yaxis = dict(title = f'{labelname}'),
            # title ='wavelength analysis of TRV data 0630 for 1st 1000rows ',
            title ='Comparison between signals',
            legend=dict(
                xanchor='left',
                yanchor='bottom',
                x=0.02,
                y=0.9,
                orientation='h',
                ),
        )
        fig.show()
    return y

def resample(df:pl.DataFrame, Timelabel, analysis_label, f_base, f_trans, mode='UP', fill_value='extrapolate', kind='linear', fpass=None, fstop=None, gpass=None, gstop=None) -> pl.DataFrame:
    '''
    df: 周波数変換したいデータフレームです。実際には、csvファイルなどを読み込んだデータになると思います。
    Timelabel: 入力したデータフレームにおける時系列のラベル名です。
    analysis_label: 周波数変換したいラベルをリストにして渡します。
    f_base: 入力したデータフレームのサンプリング周波数です。変換前の周波数とも言えます。
    f_trans: 変換後のサンプリング周波数です。
    mode: アップサンプリングかダウンサンプリングを指定します。(UP / DOWN)
    fill_value: 外挿オプションです。データの範囲外となる値を補完する場合、例えば0で埋めたり、一個前のサンプリング値で埋めることが出来ます。scipyに準拠しています。
    kind: 補間関数の設定です。scipyに準拠しています。
    fpass: ローパスフィルタの通過域端周波数です。
    fstop: 阻止域端周波数です
    gpass: 通過域最大損失量です
    gstop: 阻止域最大損失量です

    '''
    from scipy import interpolate
    import pandas as pd # [x] pandas を polarsに
    import polars as pl
    samplerate:float = 1/f_base
    filt_df:pl.DataFrame=pl.DataFrame()
    resampled_df:pl.DataFrame = pl.DataFrame()
    trans_nums = int((df[Timelabel].max() / (1 / f_base)) * (f_trans / f_base)) + 1
    print('Base Sampling rate is {0} Hz. Transformed sampling rate is {1} Hz.'.format(f_base, f_trans))
    print('Max Time is {0} s'.format(df[Timelabel].max()))
    print('Number of sampling point is {0}. It will be {1} after resampling'.format(int(df[Timelabel].max() / (1 / f_base)),trans_nums))
    
    if mode == 'UP':
        if fpass == None:
            fpass = int(f_base / 2.56)
        if fstop == None:
            fstop = int(f_base / 2)
        if gpass == None:
            gpass = 3
        if gstop == None:
            gstop = 15
        # resampled_df[Timelabel] = np.linspace(0, df[Timelabel].max(), trans_nums)
        resampled_df = resampled_df.with_columns(
            pl.Series(np.linspace(0, df[Timelabel].max(), trans_nums)).alias(Timelabel)
        )
        for label in analysis_label:
            print('Resampling {0}...'.format(label))
            function = interpolate.interp1d(df[Timelabel], df[label], fill_value=fill_value, kind=kind) # type: ignore
            temp = function(resampled_df[Timelabel])
            resampled_df =  resampled_df.with_columns(
                pl.Series(function(resampled_df[Timelabel])).alias(label)
            )
            # resampled_df[label] = function(resampled_df[Timelabel])

        # filt_df[Timelabel] = resampled_df[Timelabel]
        filt_df = filt_df.with_columns( resampled_df[Timelabel].alias(Timelabel)  )
        for idx, labelname in enumerate(analysis_label):
            filt_df = filt_df.with_columns(
                pl.Series(
                    butterlowpass(
                        x=resampled_df[labelname],
                        fpass=fpass,
                        fstop=fstop,
                        gpass=gpass,
                        gstop=gstop,
                        fs=samplerate,
                        dt=1 / f_base,
                        graphCheckflag=False,
                        labelname=labelname)
                ).alias(labelname)
            )
        return filt_df

    if mode == 'DOWN':
        if fpass == None:
            fpass = int(f_trans / 2.56)
        if fstop == None:
            fstop = int(f_trans / 2)
        if gpass == None:
            gpass = 3
        if gstop == None:
            gstop = 15
        
        # filt_df[Timelabel] = df[Timelabel]
        filt_df = filt_df.with_columns(df[Timelabel])
        for idx, labelname in enumerate(analysis_label):
            filt_df = filt_df.with_columns(
                pl.Series(
                    butterlowpass(
                        x=resampled_df[labelname], fpass=fpass,
                        fstop=fstop,
                        gpass=gpass,
                        gstop=gstop,
                        fs=samplerate,
                        dt=1 / f_base,
                        graphCheckflag=False,
                        labelname=labelname
                    )
                ).alias(labelname)
            )
            # filt_df[labelname] = butterlowpass(x=resampled_df[labelname], fpass=fpass,
            #                                                     fstop=fstop,
            #                                                     gpass=gpass,
            #                                                     gstop=gstop,
            #                                                     fs=samplerate,
            #                                                     dt=1 / f_base,
            #                                                     graphCheckflag=False,
            #                                                     labelname=labelname)
        
        resampled_df = resampled_df.with_columns(
            pl.Series(
                np.linspace(0, filt_df[Timelabel].max(), trans_nums)
            )
        )
        # resampled_df[Timelabel] = np.linspace(0, filt_df[Timelabel].max(), trans_nums)

        for label in analysis_label:
            print('Resampling {0}...'.format(label))
            function = interpolate.interp1d(filt_df[Timelabel], filt_df[label], fill_value=fill_value, kind=kind) # type: ignore
            resampled_df = resampled_df.with_columns(
                pl.Series(
                    function(resampled_df[Timelabel])
                )
            )
            # resampled_df[label] = function(resampled_df[Timelabel])

        return resampled_df
    else:
        print('Please input correct mode')
        
        raise TypeError

        # return None

#%% for debug

if __name__ == '__main__':
    # from bache_thesis_python import resample
    from bache_thesis_python import fft
    # from os import name
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly import offline
    import numpy as np
    import numpy.typing as npt
    import polars as pl
    import pandas as pd
    from pathlib import Path
    import pprint

    CURRENT_DIR = Path.cwd()
    pprint.pprint(f'__name__ = {__name__}')
    pprint.pprint(f'__name__ == "__main__" = {__name__ == "__main__"}')
    pprint.pprint(CURRENT_DIR)
    #%%
    x_ideal : npt.NDArray = np.array([i*(0.25) for i in range(0,8000)])
    # x : npt.NDArray = np.array([i*(0.25)+(np.random.rand() - 0.5 )*(1/4) for i in range(0,8000)])

    # 0
    non_uniform_seed :list = [ i*(0.25) for i in range(900) ]
    additional_array :list = [ non_uniform_seed[-1] + 0.25 + (0.2)*i for i in range(100) ]
    non_uniform_seed += additional_array
    # 1000
    additional_array :list = [ non_uniform_seed[-1] + 0.25 + (0.25)*i for i in range(950) ]
    non_uniform_seed += additional_array
    additional_array :list = [ non_uniform_seed[-1] + 0.25 + (0.30)*i for i in range(50) ]
    non_uniform_seed += additional_array
    # 2000
    additional_array :list = [ non_uniform_seed[-1] + 0.25 + (0.25)*i for i in range(200) ]
    non_uniform_seed += additional_array
    additional_array :list = [ non_uniform_seed[-1] + 0.25 + (0.2)*i for i in range(50) ]
    non_uniform_seed += additional_array
    additional_array :list = [ non_uniform_seed[-1] + 0.25 + (0.25)*i for i in range(600) ]
    non_uniform_seed += additional_array
    additional_array :list = [ non_uniform_seed[-1] + 0.25 + (0.27)*i for i in range(150) ]
    non_uniform_seed += additional_array
    # 3000
    additional_array :list = [ non_uniform_seed[-1] + 0.25 + (0.25)*i for i in range(900) ]
    non_uniform_seed += additional_array
    additional_array :list = [ non_uniform_seed[-1] + 0.25 + (0.30)*i for i in range(100) ]
    non_uniform_seed += additional_array
    # 4000
    additional_array :list = [ non_uniform_seed[-1] + 0.25 + (0.25)*i for i in range(200) ]
    non_uniform_seed += additional_array
    additional_array :list = [ non_uniform_seed[-1] + 0.25 + (0.29)*i for i in range(800) ]
    non_uniform_seed += additional_array
    # 5000
    additional_array :list = [ non_uniform_seed[-1] + 0.25 + (0.25)*i for i in range(900) ]
    non_uniform_seed += additional_array
    additional_array :list = [ non_uniform_seed[-1] + 0.25 + (0.23)*i for i in range(100) ]
    non_uniform_seed += additional_array
    # 6000
    additional_array :list = [ non_uniform_seed[-1] + 0.25 + (0.25)*i for i in range(900) ]
    non_uniform_seed += additional_array
    additional_array :list = [ non_uniform_seed[-1] + 0.25 + (0.30)*i for i in range(100) ]
    non_uniform_seed += additional_array
    # 7000
    additional_array :list = [ non_uniform_seed[-1] + 0.25 + (0.18)*i for i in range(50) ]
    non_uniform_seed += additional_array
    additional_array :list = [ non_uniform_seed[-1] + 0.25 + (0.25)*i for i in range(950) ]
    non_uniform_seed += additional_array
    # 8000
    x : npt.NDArray = np.array(non_uniform_seed)

    go.Figure(
        data = go.Scatter(x = x_ideal,y = x - x_ideal),
    ).show()
    #%%
    wave_uniform : npt.NDArray = (
        + 4*np.sin( 2*np.pi*(1/36)*x_ideal ) # 0.071
        + 10*np.sin( 2*np.pi*(1/18)*x_ideal )  # 0.056
        + 5*np.sin( 2*np.pi*(1/6.6)*x_ideal ) # 0.152
        + 8*np.cos( 2*np.pi*(1/0.3)*x_ideal ) # 3.333
        + 3*np.cos( 2*np.pi*(1/0.1)*x_ideal ) # 10
    )

    wave_non_uniform : npt.NDArray = (
        + 4*np.sin( 2*np.pi*(1/36)*x ) # 0.071
        + 10*np.sin( 2*np.pi*(1/18)*x )  # 0.056
        + 5*np.sin( 2*np.pi*(1/6.6)*x ) # 0.152
        + 8*np.cos( 2*np.pi*(1/0.3)*x ) # 3.333
        + 3*np.cos( 2*np.pi*(1/0.1)*x ) # 10
    )
    #%%
    df_to_resample = pl.DataFrame(
        dict(
            x = x,
            y = wave_non_uniform,
        )
    )

    df_result: pl.DataFrame = resample(
        df_to_resample,
        'x',
        'y',
        1/(0.25),
        1/(0.05),
        'UP',    
    )


    go.Figure(
        data = [
            go.Scatter(
                x = df_result['x'], y = df_result['y'], name = 'resampled',mode='lines'
            ),
            go.Scatter(
                x = x_ideal, y = wave_uniform,name = 'uniform',mode='lines'
            ),
            go.Scatter(
                x = x, y = wave_non_uniform,name = 'non-uniform',mode='lines'
            ),
            
        ]
    ).update_layout(
        title = 'resampled data, uniform data and non-uniform data plot',
        xaxis = dict(
            # dtick = 0.125,
            title = 'x distance(m)',
        ),
        yaxis = dict(
            # dtick = ,
            title = 'y'
        )

    ).show()
    # %%
    result_uniform = fft.calc_amp(wave_uniform,1/(0.25) )
    result_non_uniform = fft.calc_amp(wave_non_uniform,fs=1/(0.25))
    result_resampled = fft.calc_amp(np.array(df_result['y']),fs = 1/(0.05))
    figdata_fft = [
        go.Scatter(
            x = result_resampled['result_half']['freq'], y = result_resampled['result_half']['amp'], mode = 'lines', name='resampled source',
        ),
        go.Scatter(
            x = result_uniform['result_half']['freq'], y = result_uniform['result_half']['amp'], mode = 'lines', name='uniform source',
        ),
        go.Scatter(
            x = result_non_uniform['result_half']['freq'], y = result_non_uniform['result_half']['amp'], mode = 'lines', name = 'non-uniform source',
        )
    ]

    fig = go.Figure(
        data = figdata_fft,
    ).update_layout(
        title = 'uniform data and non-uniform data fft plot w.o. resampling ',
        xaxis = dict(
            # dtick = 0.125,
            title = 'freq(cycle/m)',
        ),
        yaxis = dict(
            # dtick = ,
            title = 'amplitude'
        )

    )

    fig.show()
# %%
