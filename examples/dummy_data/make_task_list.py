import os
import sys
#takes the folder of the tuning results as an argument
#then stores the results of one tune in a file of that name
#starts reading at line 9 of minimum_tnc_1_1.txt in the folder

if len(sys.argv) != 3:
    print('invalid arguments to make_task_list.py')

filename = sys.argv[1]
task_number = sys.argv[2]

f = open(filename, "w")
for i in range(int(task_number)):
    f.write("bash " + os.getcwd() + "/cori_bash/run_one.sh " + str(i) + "\n")
