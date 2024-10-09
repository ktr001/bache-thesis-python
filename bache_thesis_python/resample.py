## reference : https://qiita.com/Qooniee/items/7dde8602ca41a1fd5790
import numpy as np

def butterlowpass(x, fpass, fstop, gpass, gstop, fs, dt, graphCheckflag=False, labelname='Signal[-]'):
    from scipy import signal
    import matplotlib.pyplot as plt
    # [ ] matplotlib を plotlyに
    import numpy as np

    '''
    バターワースを用いたローパスフィルタ
    filtfilt関数により位相ずれを防ぐ
    (順方向と逆方向からフィルタをかけて位相遅れを相殺)
    :param x: 入力データ
    :param fpass: 通過域端周波数[Hz]
    :param fstop: 阻止域端周波数[Hz]
    :param gpass: 通過域最大損失量[dB]
    :param gstop: 阻止域最大損失量[dB]
    :param fs: サンプリング周波数[Hz]
    :param dt: サンプリング間隔[s]
    :param checkflag: グラフ生成ON/OFF
    :param labelname: 信号ラベル名
    :return:　フィルター後データ
    '''

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
        plt.figure(figsize = (12, 5))
        plt.title('Comparison between signals')
        plt.plot(time, x, color='black', label='Raw signal')
        plt.plot(time, y, color='red', label='Filtered signal')
        plt.xlabel('Time[s]')
        plt.ylabel(labelname)
        plt.show()
    return y

def resample(df, Timelabel, analysis_label, f_base, f_trans, mode='UP', fill_value='extrapolate', kind='linear', fpass=None, fstop=None, gpass=None, gstop=None):
    from scipy import interpolate
    import pandas as pd # [ ] pandas を polarsに
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
    
    
    