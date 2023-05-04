import os
import sys
#takes the folder of the tuning results as an argument
#then stores the results of one tune in a file of that name in results/many_tunes
#starts reading at line 9 of minimum_tnc_1_1.txt in the folder

if len(sys.argv) != 2:
    print('invalid arguments to gather_tune_data.py')

filename = sys.argv[1]
tune_output = open(filename + '/minimum_tnc_1_1.txt', 'r').readlines()

params = []
vars = []
is_boundary = []
chi2 = tune_output[2].split()[2]

#This is where apprentice writes tunes, one param per line
place = 8
while place < len(tune_output):
    line = tune_output[place].split()
    #weird error--apprentice makes a -> b'a'. undo here
    print(line[0], line[0][2:-1])
    params.append(line[0][2:-1])
    vars.append(line[1])
    #Right now will remember if any tune was ONBOUND
    is_boundary = is_boundary or (line[3] == 'ONBOUND')
    place = place + 1
#if file is not created, create it and write param names on top
dest_filepath= "../../results/many_tunes/"+filename+".csv"
if(not os.path.exists(dest_filepath)):
    f = open(dest_filepath, "w")
    f.write(','.join([str(s) for s in params]))
    f.write(',ONBOUND,chi2\n')
    f.close()

#write the var values, appending this time
f = open(dest_filepath, "a")
f.write(','.join(vars))
f.write(',')
f.write(str(is_boundary))
f.write(',')
f.write(chi2)
f.write('\n')
f.close()