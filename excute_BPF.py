'''時刻歴振動データにBandpass filterを適用'''
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

# %%

# ####### practice filter ######

# samplerate = 100
# x = np.arange(0, 1000) / samplerate                 # 波形生成のための時間軸の作成
# # data = np.random.normal(loc=0, scale=1, size=len(x)) #ガウシアンノイズを生成
# data = np.sin(2*np.pi*0.25*x) + np.sin(2*np.pi*1*x) + np.sin(2*np.pi*4*x) + np.sin(2*np.pi*8*x)
 
# fp = np.array([0.5, 8])     #通過域端周波数[Hz]※ベクトル
# fs = np.array([0.01,16 ])     #阻止域端周波数[Hz]※ベクトル
# gpass = 3                       #通過域端最大損失[dB]
# gstop = 40                      #阻止域端最小損失[dB]
 
# data_filt = filter_function.bandpass(data, samplerate, fp, fs, gpass, gstop)

# figdata:list[go.Scatter] = [
#     go.Scatter(x = x[0:1600], y = data[0:1600]),
#     go.Scatter(x = x[0:1600], y = data_filt[0:1600])
#     ] 
# fig:go.Figure=go.Figure(data = figdata)
# fig.show()

# # %%
# ###### FFT (debug)

# F_rand = np.fft.fft(data)
# Amp_rand = np.abs( F_rand / (len(x) / 2) )
# F_filt = np.fft.fft(data_filt)
# Amp_filt = np.abs( F_filt / (len(x) / 2) )

# freq_rand = np.fft.fftfreq(len(x), d= 1/samplerate)
# half_N = len(freq_rand) // 2
# fft_figdata:list[go.Scatter] = [
#     go.Scatter(x = freq_rand[0:half_N], y = Amp_rand[0:half_N]),
#     go.Scatter(x = freq_rand[0:half_N], y = Amp_filt[0:half_N]),
# ]
# fft_fig:go.Figure = go.Figure(data = fft_figdata)
# fft_fig.show()

# ##### FFT end

#%%

path_to_ang_vel_0629_raw:str = "/home/iori/daxue/bache_thesis/20240629_down_Futamata_to_Shinjohara/ang_vel_0629_raw.csv"

# with open(path_to_ang_vel_0629_raw) as f:
#     pprint(f.read())
# ref  https://note.nkmk.me/python-numpy-loadtxt-genfromtxt-savetxt/
rawdata_array:npt.NDArray =  np.loadtxt(path_to_ang_vel_0629_raw,delimiter = ',',skiprows=1,usecols=[1,2,3]).T
timerow:npt.NDArray =  np.loadtxt(path_to_ang_vel_0629_raw,delimiter = ',',skiprows=1,usecols=[0],dtype = object).T
num_of_data :int = len(rawdata_array[0])
# chrono_data :npt.NDArray = np.loadtxt(path_to_ang_vel_0629_raw,delimiter = ',',skiprows=1,usecols=0,dtype='str').T
# pprint(rawdata_array)
# pprint(chrono_data)

# ref https://qiita.com/flcn-x/items/0c84afb30dc62aa97e3d
# %%
SAMPLE_FREQ : int = 100 # hz
FREQ_PASS : npt.NDArray = np.array([0.5, 8]) # frequency to allow to path
FREQ_S : npt.NDArray = np.array([0.24, 16]) # frequency not to allow to path
chrono_secuence :npt.NDArray = np.arange(0,num_of_data) / 100 # desiably generated from csv's chronological data, but can't convert the text(e.g. "08:27:20.206") to time.
GPASS = 1                       #通過域端最大損失[dB]
GSTOP = 40                      #阻止域端最小損失[dB]

raw_data_x :npt.NDArray = rawdata_array[0]
raw_data_y :npt.NDArray = rawdata_array[1]
raw_data_z :npt.NDArray = rawdata_array[2]

filt_data_x :npt.NDArray = filter_function.bandpass(raw_data_x,SAMPLE_FREQ,FREQ_PASS,FREQ_S,GPASS,GSTOP)
filt_data_y :npt.NDArray = filter_function.bandpass(raw_data_y,SAMPLE_FREQ,FREQ_PASS,FREQ_S,GPASS,GSTOP)
filt_data_z :npt.NDArray = filter_function.bandpass(raw_data_z,SAMPLE_FREQ,FREQ_PASS,FREQ_S,GPASS,GSTOP)

# %%

figdata:list[go.Scatter] = [
    go.Scatter(x = chrono_secuence, y = raw_data_z),
    go.Scatter(x = chrono_secuence, y = filt_data_z),
    ] 
fig:go.Figure=go.Figure(data = figdata)
fig.show()
# %%

###### FFT (debug)

F_raw = np.fft.fft(raw_data_z)
Amp_raw = np.abs( F_raw / (num_of_data / 2) )
F_filt = np.fft.fft(filt_data_z)
Amp_filt = np.abs( F_filt / (num_of_data / 2) )

freq = np.fft.fftfreq(num_of_data, d= 1/SAMPLE_FREQ)
n_freq_half : int = len(freq) // 2
fft_figdata:list[go.Scatter] = [
    go.Scatter(x = freq[0:n_freq_half], y = Amp_raw[0:n_freq_half]),
    go.Scatter(x = freq[0:n_freq_half], y = Amp_filt[0:n_freq_half]),
]
fft_fig:go.Figure = go.Figure(data = fft_figdata)
fft_fig.show()

##### FFT end
#%%

path_to_ang_vel_0629_BPF:str = "/home/iori/daxue/bache_thesis/20240629_down_Futamata_to_Shinjohara/ang_vel_0629_BPF.csv"
filt_data = np.array([timerow,filt_data_x,filt_data_y,filt_data_z]).T
np.savetxt(path_to_ang_vel_0629_BPF,filt_data,delimiter=',',fmt=['%s','%.18e','%.18e','%.18e'])

#%%
with open(path_to_ang_vel_0629_BPF) as f:
    pprint(f.read())
#%%