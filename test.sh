#!/bin/sh
echo start
function move_file(){
    date=${1: 0-12:8}
    dir1="./$date"
    if [ ! -d "$dir1" ]; then
    mkdir $dir1
    fi
    mv $1 ./$date
}
read -p "please give the rar file name in full " rar_file
echo "filename is ${rar_file}"
dir="./${rar_file%.*}"
if [ ! -d "$dir" ];then
mkdir $dir
fi
unrar e ./$rar_file $dir/
cd $dir
files=$(ls)
for file in $files;
do
move_file $file
done
cd ..
python ./wash.py ${dir: 2}