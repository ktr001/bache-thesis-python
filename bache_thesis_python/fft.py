#%%
import numpy as np
import numpy.typing as npt
import scipy

from  plotly import graph_objects  as go
from scipy import signal
import scipy.signal
# import scipy.signal

from pathlib import Path
import pprint
CURRENT_DIR = Path.cwd()
pprint.pprint(f'__name__ = {__name__}')
pprint.pprint(CURRENT_DIR)


# %%
# 信号周波数
fc:float = 100 # 決め打ち
#%%
# def output_fft(x:npt.NDArray, N:int, fs:float) -> tuple[npt.NDArray[np.floating],npt.NDArray[np.floating]]:
#     ''' fs : for sampling freq '''

#     if N < fs/fc :
#         raise ValueError(f'N must be larger than fs/fc, now N = {N},fs/fc={fs}/{fc}= {fs/fc} ')

#     X:npt.NDArray[np.floating] = fft(x,n=N)
#     # FFT実行(N点)
#     # 周波数軸の生成
#     # 1[周波数index]あたりの周波数間隔df=fs/N
#     df:float = fs/N

#     # [周波数index]生成
#     sampleIndex:npt.NDArray[np.int128] = np.arange(start=0, stop=N)
#     # [周波数index] --> 周波数間隔を反映
#     f:npt.NDArray[np.floating] = sampleIndex*df
#     # FFTシフト検証（ X=fft(x,N) ）
#     Shifted_X = fftshift(X)
#     # FFTシフト後の[周波数index]生成(//は整数割り)
#     Shifted_sampleIndex = np.arange(-N//2, N//2)
#     # FFTシフト後の[周波数index] --> 周波数間隔dfへ
#     Shifted_f = Shifted_sampleIndex*df
#     return Shifted_f,Shifted_X
# %%
# 高速フーリエ変換
def calc_amp(data:npt.NDArray, fs:float) -> dict[str,dict[str,npt.NDArray]]:
    '''フーリエ変換して振幅スペクトルを計算する関数
    fullの周波数/振幅と、周波数の後半の成分を返す。
    そこそこ正確に結果が返ってくるっぽい？
    '''
    N = len(data)
    window = scipy.signal.get_window('hann', Nx = N)
    F = np.fft.fft(data * window)
    freq = np.fft.fftfreq(N, d=1/fs) # 周波数スケール
    F = F / (N / 2) # フーリエ変換の結果を正規化
    F = F * (N / sum(window)) # 窓関数による振幅減少を補正する
    Amp = np.abs(F) # 振幅スペクトル
    num_of_freq_half:int = len(freq) // 2
    return {
        'result_full':{
            'amp_full':Amp,
            'freq_full':freq,
        },
        'result_half':{
            'amp':Amp[0:num_of_freq_half],
            'freq':freq[0:num_of_freq_half],
        },
    }
# %%
