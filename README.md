Introdunction:
--------------------------
test.sh is a shell script that unrar the given rar file and activate wash.py.

wash.py washes the data and generates a summary csv file.

Our rar file, put in the same folder as the scripts, contains an amount of csv files whose names contain date information in yyyymmdd format.

data_structure.txt shows data structure in each of csv file.

The two test .sh files are test versions that generates washed csv for 20200803 under relative directory in wash_and_rar


Working period:
-------------------------
2020/8/18 to 2020/8/19

Points covered：
-------------
    1. Shell script usage
    2. Data washing
    3. Powerful pathlib.Path
