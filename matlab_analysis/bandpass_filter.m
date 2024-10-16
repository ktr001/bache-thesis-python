% テキスト ファイルからのデータのインポート
ang_vel_0629_raw = readtimetable("\\wsl.localhost\Ubuntu\home\iori\daxue\bache_thesis\20240629_down_Futamata_to_Shinjohara\ang_vel_0629_raw.csv", "RowTimes", "localTimeStamp");

% 結果の表示
ang_vel_0629_raw

% ang_vel_0629_raw = removevars(timetable2table(ang_vel_0629_raw),"localTimeStamp");
% ang_vel_0629_raw = ang_vel_0629_raw(1:9999,:)
% ang_vel_0629_raw = rows2vars(ang_vel_0629_raw)
% ang_vel_roll = ang_vel_0629_raw(3,:)
num_of_datas = size(ang_vel_roll,2)
fs = 100;
t = 0:1/fs:num_of_datas;
% 
% table2array(ang_vel_roll)
% bandpass(ang_vel_roll,[0.5,8],fs)

ang_vel_0629_raw = ang_vel_0629_raw(1:9999,:)
bandpass(ang_vel_0629_raw,[0.5,8],fs)