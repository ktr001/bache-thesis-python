
#%%
import numpy as np
import numpy.typing as npt
import scipy
from scipy.fftpack import fft
from scipy.fftpack import fftshift
# %%
from  plotly import graph_objects  as go
# %%
# from scipy import signal
import scipy.signal
#%%
# サンプリング周波数
fs = 100 #from the app setting
# 信号周波数
fc = 100 # 決めうち

N:int = 1000
if N < fs/fc :
    raise ValueError(f'N must be larger than fs/fc, now N = {N},fs/fc={fs}/{fc}= {fs/fc} ')

# 時間ポイント( 長さ=2[s]/(1/fs)=2*32*10=640点 )
t:np.ndarray = np.arange(start=0, stop=2, step=1/fc)
# 信号
x:np.ndarray = np.cos(2*np.pi*fc*t) + 2 * np.cos(7 * np.pi*fc*t)
# x:np.ndarray = np.cos(2*np.pi*fc*t) + np.cos(5*2*np.pi*fc*t)

#%%
# FFT実行(N点)
X = fft(x, N)
# 周波数軸の生成
# 1[周波数index]あたりの周波数間隔df=fs/N
df = fs/N

# [周波数index]生成
sampleIndex = np.arange(start=0, stop=N)
# [周波数index] --> 周波数間隔を反映
f = sampleIndex*df
# %%
# FFTシフト検証（ X=fft(x,N) ）
Shifted_X = fftshift(X)
# FFTシフト後の[周波数index]生成(//は整数割り)
Shifted_sampleIndex = np.arange(-N//2, N//2)
# FFTシフト後の[周波数index] --> 周波数間隔dfへ
Shifted_f = Shifted_sampleIndex*df
# %%

figdata:list[go.Scatter]=[] # init
figdata.append(
    go.Scatter(
        x=Shifted_f,y=np.abs(Shifted_X)/N
    )
)
fig:go.Figure=go.Figure(data=figdata)
fig.show()
# %%
window:npt.NDArray = scipy.signal.get_window('hann', Nx = len(t) )
# %%
go.Figure(
    data = [
        go.Scatter(x = t, y = x),
        go.Scatter(x = t, y = x * window)
        ]
).show()
# %%



#%% ################ export function here #####################
def output_fft(x:npt.NDArray, N:int, fs:float) -> tuple[npt.NDArray[np.floating],npt.NDArray[np.floating]]:

    if N < fs/fc :
        raise ValueError(f'N must be larger than fs/fc, now N = {N},fs/fc={fs}/{fc}= {fs/fc} ')

    X:npt.NDArray[np.floating] = fft(x,n=N)
    # FFT実行(N点)
    # 周波数軸の生成
    # 1[周波数index]あたりの周波数間隔df=fs/N
    df:float = fs/N

    # [周波数index]生成
    sampleIndex:npt.NDArray[np.int128] = np.arange(start=0, stop=N)
    # [周波数index] --> 周波数間隔を反映
    f:npt.NDArray[np.floating] = sampleIndex*df
    # FFTシフト検証（ X=fft(x,N) ）
    Shifted_X = fftshift(X)
    # FFTシフト後の[周波数index]生成(//は整数割り)
    Shifted_sampleIndex = np.arange(-N//2, N//2)
    # FFTシフト後の[周波数index] --> 周波数間隔dfへ
    Shifted_f = Shifted_sampleIndex*df
    return Shifted_f,Shifted_X
#%% ################ export function #####################

Shifted_results:tuple[npt.NDArray[np.floating],npt.NDArray[np.floating]] = output_fft(x * window, N=N, fs = fs)
#%%
go.Figure(
    data = [
        go.Scatter( x = Shifted_results[0], y = np.abs(Shifted_results[1])/N ),
        # go.Scatter( x=Shifted_f, y=np.abs(Shifted_X)/N/14 )
    ]
).show()

# %%
