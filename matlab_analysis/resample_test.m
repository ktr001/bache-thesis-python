%%
FILEPATH  = "\\wsl.localhost\Ubuntu\home\iori\daxue\bache_thesis\20230630_軌道変位データ\TGdata20230630_converted.csv";
%% FILEPATH  = "\\wsl.localhost\Ubuntu\home\iori\daxue\bache_thesis\20230630_軌道変位データ\TGdata_freqtestdata_1st1000.csv";
DELIMITERIN = ',';
TGDATA = importdata(FILEPATH,DELIMITERIN)
FS = 1/(0.25);

%%
tx = TGDATA.data(:,1)
x = TGDATA.data(:,2:8)
%%
[y,ty] = resample(x,tx,FS)
%%
plot(tx,x,'*',ty,y,'o')

%%
% OUTPUT_FILE = "\\wsl.localhost\Ubuntu\home\iori\daxue\bache_thesis\20230630_軌道変位データ\TGdata_resampled.csv";

resampled_table = array2table([ty,y])
writetable(resampled_table,OUTPUT_FILE)