## reference : https://qiita.com/Qooniee/items/7dde8602ca41a1fd5790
import numpy as np

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

def resample(df, Timelabel, analysis_label, f_base, f_trans, mode='UP', fill_value='extrapolate', kind='linear', fpass=None, fstop=None, gpass=None, gstop=None):
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
    import pandas as pd # [ ] pandas を polarsに
    import polars as pl
    samplerate:float = 1/f_base
    filt_df, resampled_df = pd.DataFrame(),pd.DataFrame()
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
        resampled_df[Timelabel] = np.linspace(0, df[Timelabel].max(), trans_nums)
        for label in analysis_label:
            print('Resampling {0}...'.format(label))
            function = interpolate.interp1d(df[Timelabel], df[label], fill_value=fill_value, kind=kind) # type: ignore
            resampled_df[label] = function(resampled_df[Timelabel])

        filt_df[Timelabel] = resampled_df[Timelabel]
        for idx, labelname in enumerate(analysis_label):
            filt_df[labelname] = butterlowpass(x=resampled_df[labelname], fpass=fpass,
                                                                fstop=fstop,
                                                                gpass=gpass,
                                                                gstop=gstop,
                                                                fs=samplerate,
                                                                dt=1 / f_base,
                                                                graphCheckflag=False,
                                                                labelname=labelname)
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
        
        filt_df[Timelabel] = df[Timelabel]
        for idx, labelname in enumerate(analysis_label):
            filt_df[labelname] = butterlowpass(x=resampled_df[labelname], fpass=fpass,
                                                                fstop=fstop,
                                                                gpass=gpass,
                                                                gstop=gstop,
                                                                fs=samplerate,
                                                                dt=1 / f_base,
                                                                graphCheckflag=False,
                                                                labelname=labelname)
        resampled_df[Timelabel] = np.linspace(0, filt_df[Timelabel].max(), trans_nums)
        for label in analysis_label:
            print('Resampling {0}...'.format(label))
            function = interpolate.interp1d(filt_df[Timelabel], filt_df[label], fill_value=fill_value, kind=kind) # type: ignore
            resampled_df[label] = function(resampled_df[Timelabel])

        return resampled_df
    else:
        print('Please input correct mode')
        return None
    
    
    