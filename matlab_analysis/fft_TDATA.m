%%
SOURCE_FILE_PATH = "\\wsl.localhost\Ubuntu\home\iori\daxue\bache_thesis\20230630_軌道変位データ\TGdata_resampled.csv";
DELIMITERIN = ',';
TGDATA = importdata(SOURCE_FILE_PATH,DELIMITERIN)
%%
FS = 1/(0.25);
L = length(TGDATA.data)
START_KILO = 114.5
%%
DATA_to_FFT = TGDATA.data(:,2:8)
DATA_time = TGDATA.data(:,1) - START_KILO
%%
Y = fft(DATA_to_FFT)
plot(FS*(-L/2:L/2 -1)*L , abs(fftshift(Y)),"LineWidth",3)