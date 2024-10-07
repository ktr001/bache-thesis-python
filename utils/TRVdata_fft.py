#%%
from os import name
import datetime
from wave import Wave_write
import plotly.graph_objects as go
from plotly import offline
import numpy as np
import numpy.typing as npt
# from bache_thesis_python import *
import polars as pl
from pathlib import Path
import pprint

from add_kilometre import PATH_TO_DATA_DIR
from convert_KMtoMetre import PATH_TO_0630_DATA_DIR, SOURCE_0630_FILE
from excute_BPF import SAMPLE_FREQ
CURRENT_DIR = Path.cwd()
pprint.pprint(f'__name__ = {__name__}')
pprint.pprint(f'__name__ == "__main__" = {__name__ == "__main__"}')
pprint.pprint(CURRENT_DIR)

#%%
SOURCE_0630_FILE :str= PATH_TO_0630_DATA_DIR + "TGdata_frewtestdata_1st1000.csv"
#%%
###### FFT (debug)
def graph_fft(raw_data):
    num_of_data = len(raw_data)
    SAMPLE_FREQ = 1/(0.25) #空間周波数[1/m]
    F = np.fft.fft(raw_data)
    Amp = np.abs( F / (num_of_data / 2) )

    freq = np.fft.fftfreq(num_of_data, d= 1/SAMPLE_FREQ)
    n_freq_half : int = len(freq) // 2
    fft_figdata:list[go.Scatter] = [
        go.Scatter(x = freq[0:n_freq_half], y = Amp[0:n_freq_half]),
    ]
    fft_fig:go.Figure = go.Figure(data = fft_figdata)
    fft_fig.show()

def dft(w,t,G):
    def expi(x):
        return np.exp(complex(0.,x))
    res = 0.+0.j
    for i in range(len(t)-1):
        tx,ty = t[i],t[i+1]
        Gx,Gy = G[i],G[i+1]
        dt = ty-tx
        exwdt = expi(-w*dt)
        d = (complex(1.0,-w*dt) - exwdt )/(w**2*dt)
        dc= d.conjugate()                
        res += (Gx*d + Gy*dc * exwdt) * expi(-w*tx)
    return w, res.real, res.imag


##### FFT end
# %%
t = np.arange(0,50,0.25)
wave = np.sin(2*np.pi*t) + 0.5*np.sin(2*0.5*np.pi*t)
#%%
graph_fft(wave)
# %%
# pprint.pprint(dft(1,t,wave))
freqlist = np.arange(0.1,2,step=0.1)
result_amp = [dft(spfreq,t,wave)[1] for spfreq in freqlist]
# %%
go.Figure(
    data = [
        go.Scatter(
            x = freqlist,
            y = result_amp,
        )
    ]
).show()
#%%
df_twist = pl.read_csv(SOURCE_0630_FILE).select(["キロ程(meter)","平面性(生波形)"])
graph_fft(df_twist["平面性(生波形)"])

# %%
