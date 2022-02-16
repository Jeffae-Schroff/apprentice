import os
import sys
#takes the folder of the tuning results as an argument
#then stores the results of one tune in a file of that name
#starts reading at line 9 of minimum_tnc_1_1.txt in the folder

if len(sys.argv) != 2:
    print('invalid arguments to gather_tune_data.py')

filename = sys.argv[1]

tune_output = open(filename + '/minimum_tnc_1_1.txt', 'r').readlines()

params = []
vars = []
#Due to the format of files apprentice outputs
place = 8
while place < len(tune_output):
    line = tune_output[place].split()
    params.append(line[0])
    vars.append(line[1])
    place = place + 1

#if file is not created, create it and write param names on top

if(not os.path.exists("many_tunes/"+filename)):
    f = open("many_tunes/"+filename, "w")
    for p in params:
        f.write(p.ljust(20))
    f.write('\n')
    f.close()

#write the var values, appending this time
f = open("many_tunes/"+filename, "a")
for v in vars:
    f.write(str(v).ljust(20))
f.write('\n')
f.close()