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
# date="$(date +%Y%m%d)"


gen_one_day(){
    date=$1
    for file in $(ls /dat5/all/L1/Future/JSY/RAW/realtime_pm/rar_data/*"$date"*.rar);
    do
    bash /dat5/all/L1/Future/JSY/RAW/realtime_pm/rar_data/unrar_and_wash/unrar.sh "$file"
    done
    /opt/anaconda/envs/alphadig/bin/python /dat5/all/L1/Future/JSY/RAW/realtime_pm/rar_data/unrar_and_wash/wash.py -t /dat5/all/L1/Future/JSY/v1.0/data -s "$date" -e "$date"
}


gen_for_period(){
    for date in $(awk -v s=$1 -v e=$2 '$1>=s && $1<e {print $0}' /dat/all/Future/WIND/list/tradedays.csv);
    do 
    gen_one_day "$date"
    done
}


gen_for_period 20200831 20200901
