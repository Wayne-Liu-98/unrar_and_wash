#!/bin/sh

###
 # @version: Python 3.7.3
 # @Author: Louis
 # @Date: 2020-08-27 14:30:37
 # @LastEditors: Wayne
 # @LastEditTime: 2020-08-27 15:36:02
### 
split_dir(){
    date=${1: 0-12:8}
    split=/${date: 0: 4}/${date: 4: 2}/${date: 6: 2}/
    echo "$split"
}
today="20200804"
#cd /dat5/all/L1/Future/JSY/RAW/realtime_pm/rar_data || exit
for file in $(ls /dat5/all/L1/Future/JSY/RAW/realtime_pm/rar_data/*"$today"*.rar);
do
bash /dat5/all/L1/Future/JSY/RAW/realtime_pm/rar_data/unrar_and_wash/unrar_test.sh "$file"
done
/opt/anaconda/envs/alphadig/bin/python /dat5/all/L1/Future/JSY/RAW/realtime_pm/rar_data/unrar_and_wash/wash.py --source_path /dat5/all/L1/Future/JSY/RAW/realtime_pm/rar_data/unrar_and_wash  -t /dat5/all/L1/Future/JSY/RAW/realtime_pm/rar_data/unrar_and_wash/result -s "$today" -e "$today"