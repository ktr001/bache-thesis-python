%%
SOURCE_FILE_PATH = "\\wsl.localhost\Ubuntu\home\iori\daxue\bache_thesis\20230630_軌道変位データ\TGdata_resampled_byMatLab_relabeled.csv";
DELIMITERIN = ',';
TGDATA = importdata(SOURCE_FILE_PATH,DELIMITERIN)
%%
FS = 1/(0.25);
L = length(TGDATA.data)
START_KILO = 114.5
%%
% DATA_to_FFT = TGDATA.data(:,2:8)
DATA_to_FFT = TGDATA.data(:,[8,7]) % 平面性,水準
DATA_time = TGDATA.data(:,1) - START_KILO

%% welchのPSD推定
pxx = pwelch(DATA_to_FFT);
pwelch(DATA_to_FFT)