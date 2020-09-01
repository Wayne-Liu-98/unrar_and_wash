#!/bin/sh

###
 # @version: Python 3.7.3
 # @Author: Louis
 # @Date: 2020-08-27 14:30:37
 # @LastEditors: Wayne
 # @LastEditTime: 2020-08-27 15:37:44
### 
echo start
# function move_file(){
#     date=${1: 0-12:8}
#     dir1="./$date"
#     if [ ! -d "$dir1" ]; then
#     mkdir $dir1
#     fi
#     mv $1 ./$date
# }
split_dir(){
    date=${1: 0-12:8}
    split=/${date: 0: 4}/${date: 4: 2}/${date: 6: 2}/
    echo "$split"
}
rar_file=$1
echo "filename is ${rar_file}"
echo split_dir "$rar_file"
sub_dir=$(split_dir "$rar_file")
dir="/dat5/all/L1/Future/JSY/v0.0/data"$sub_dir
echo "$dir"
if [ ! -d "$dir" ];then
mkdir "$dir"
fi
unrar e "$rar_file" "$dir" -o+
# cd $dir
# files=$(ls)
# for file in $files;
# do
# move_file $file
# done
# cd -
# rm -r $dir
# /opt/anaconda/envs/alphadig/bin/python ./wash.py ${dir: 2}
