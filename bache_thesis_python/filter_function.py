from scipy import signal
from pprint import pprint

#バターワースフィルタ（バンドパス）
def bandpass(x, samplerate:float, fp, fs, gpass:float, gstop:float):
    fn = samplerate / 2                                     #ナイキスト周波数
    wp = fp / fn                                            #ナイキスト周波数で通過域端周波数を正規化
    ws = fs / fn                                            #ナイキスト周波数で阻止域端周波数を正規化
    N, Wn = signal.buttord(wp, ws, gpass, gstop)  #オーダーとバターワースの正規化周波数を計算
    pprint("N=")
    pprint(N)
    pprint("Wn=")
    pprint(Wn)
    b, a = signal.butter(N, Wn, "band")     #フィルタ伝達関数の分子と分母を計算
    pprint("b=")
    pprint(b)
    pprint("a=")
    pprint(a)
    y = signal.filtfilt(b, a, x)                  #信号に対してフィルタをかける
    pprint("y=")
    pprint(y)
    return y                                                        #フィルタ後の信号を返す