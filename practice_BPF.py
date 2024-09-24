# %%

from pathlib import Path
import pprint
import time
pprint.pprint(object=Path.cwd())

# %%
import numpy as np
import numpy.typing as npt
from bache_thesis_python import *
from pprint import pprint
import plotly.graph_objects as go


from scipy.fftpack import fft
from scipy.fftpack import fftshift
# %%

samplerate = 25600
x = np.arange(0, 12800) / samplerate                 # 波形生成のための時間軸の作成
data = np.random.normal(loc=0, scale=1, size=len(x)) #ガウシアンノイズを生成
 
fp = np.array([1000, 3000]) * 0.111375     #通過域端周波数[Hz]※ベクトル
fs = np.array([500, 6000]) * 0.111375    #阻止域端周波数[Hz]※ベクトル
gpass = 3                       #通過域端最大損失[dB]
gstop = 40                      #阻止域端最小損失[dB]
 
data_filt = filter_function.bandpass(data, samplerate, fp, fs, gpass, gstop)

figdata:list[go.Scatter] = [
    go.Scatter(x = x, y = data),
    go.Scatter(x = x, y = data_filt)
    ] 
fig:go.Figure=go.Figure(data = figdata)
fig.show()
# %%

samplerate = 25600
x = np.arange(0, 25600 * 10) / samplerate                 # 波形生成のための時間軸の作成
data = np.random.normal(loc=0, scale=1, size=len(x)) #ガウシアンノイズを生成
 
fp = np.array([100, 300])      #通過域端周波数[Hz]※ベクトル
fs = np.array([50, 600])     #阻止域端周波数[Hz]※ベクトル
gpass = 3                       #通過域端最大損失[dB]
gstop = 40                      #阻止域端最小損失[dB]
 
data_filt = filter_function.bandpass(data, samplerate, fp, fs, gpass, gstop)

figdata:list[go.Scatter] = [
    go.Scatter(x = x, y = data),
    go.Scatter(x = x, y = data_filt)
    ] 
fig:go.Figure=go.Figure(data = figdata)
fig.show()

# %%